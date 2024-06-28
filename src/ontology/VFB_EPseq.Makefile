## Customize Makefile settings for VFB_EPseq
##
## If you need to customize your Makefile, make
## changes here rather than in the main Makefile

# uses aspects of scRNAseq pipeline, such as schema (extended here), but expected to be run one dataset at a time to make metadata and expression ontologies after some semi-automated pre-processing. Release process updates imports for all ontology files at once and produces all release files.

DATADIR = ../data_files
EXPDIR = expression_data
METADATADIR = metadata_files
ONTOLOGYDIR = ontology_files
DATASET = PRJNA480794

$(EXPDIR) $(METADATADIR) $(ONTOLOGYDIR):
	mkdir -p $@

LINKML = linkml-data2owl -s VFB_EPseq_schema.yaml

.PHONY: install_linkml
install_linkml:
	python3 -m pip install linkml-owl

.PHONY: update_schema
update_schema: install_requirements
	wget https://raw.githubusercontent.com/VirtualFlyBrain/vfb-scRNAseq-ontology/main/src/ontology/VFB_scRNAseq_schema.yaml -O VFB_scRNAseq_schema.yaml

.PHONY: install_requirements
install_requirements:
	python3 -m pip install -r $(SCRIPTSDIR)/requirements.txt


################## EXPRESSION FILE

# First make a correctly-formatted $(EXPDIR)/$(DATASET)_expression_FINAL.tsv)

.PHONY: process_expdata
# split expression data into chunked sample tsvs - RUN THIS FIRST
process_expdata: | $(EXPDIR) $(METADATADIR)
	python3 $(SCRIPTSDIR)/process_expression_data.py $(DATASET)

# gene expression owl files for datasets that have 'sample' expression data tsvs or ofns (names are dataset_PRJxxxxxxx_x-sample_SAMxxxxxxx_chunk_x)
DATASET_EXP_FILES = $(sort $(filter-out sample_%,$(subst -,.owl ,$(wildcard $(EXPDIR)/*.tsv))) $(filter-out sample_%,$(subst -,.owl ,$(wildcard $(EXPDIR)/*.ofn))))

.PHONY: make_expression_files
# make ofns from tsvs and merge into owl files - RUN THIS SECOND
make_expression_files: make_exp_ofns $(DATASET_EXP_FILES)

.PHONY: make_exp_ofns
# check whether ofn exists for each sample tsv, delete tsv if true, make ofn then delete tsv if false.
make_exp_ofns: install_linkml update_schema
	apt-get update
	apt-get -y install parallel
	find $(EXPDIR) -name "*.tsv" | parallel -j 5 ' \
		if [ -e {.}.ofn ]; then \
			rm {}; \
		else \
			$(LINKML) -C ExpressionPattern {} -o {.}.ofn && rm {}; \
		fi'

# merge and annotate sample ofns for each dataset chunk
# need to reformat expression annotations as these don't get the right types from linkml
$(EXPDIR)/dataset_%.owl:
	$(ROBOT) merge --inputs "$(EXPDIR)/dataset_$**.ofn" \
	annotate --ontology-iri "http://purl.obolibrary.org/obo/VFB_EPseq/$@" \
	-o $(TMPDIR)/$*-exp-tmp.ofn &&\
	cat $(TMPDIR)/$*-exp-tmp.ofn | sed -e 's/(neo_custom:expression_\([a-z]\+\) "\([0-9]\+\.[0-9]\+\)")/(neo_custom:expression_\1 "\2"^^xsd:float)/g' -e 's/(neo_custom:hide_in_terminfo "\([a-z]\+\)")/(neo_custom:hide_in_terminfo "\1"^^xsd:boolean)/g' > $@ &&\
	$(ROBOT) convert -i $@ --format owl -o $@ &&\
	$(ROBOT) convert -i $@ --format owl -o $@.gz &&\
	rm -f $(wildcard $(EXPDIR)/dataset_$**.ofn) $(TMPDIR)/$*-exp-tmp.ofn

################### metadata file

# build metadata ontology for dataset
$(ONTOLOGYDIR)/VFB_EPseq_$(DATASET).owl: update_schema install_requirements | $(TMPDIR)
	$(LINKML) -C ExpressionPattern $(DATADIR)/$(DATASET)/$(DATASET)_sample_metadata_FINAL.tsv -o $(ONTOLOGYDIR)/$(DATASET)_sample_metadata.ofn &&\
	$(LINKML) -C DatasetEP $(DATADIR)/$(DATASET)/$(DATASET)_dataset_metadata_FINAL.tsv -o $(ONTOLOGYDIR)/$(DATASET)_dataset_data.ofn &&\
	$(ROBOT) merge \
	--input $(ONTOLOGYDIR)/$(DATASET)_sample_metadata.ofn \
	--input $(ONTOLOGYDIR)/$(DATASET)_dataset_data.ofn \
	--include-annotations true --collapse-import-closure false \
	annotate --ontology-iri http://virtualflybrain.org/data/VFB/OWL/dataset_$(DATASET).owl \
	convert --format owl \
	-o $@ &&\
	rm $(ONTOLOGYDIR)/$(DATASET)_sample_metadata.ofn $(ONTOLOGYDIR)/$(DATASET)_dataset_data.ofn

################# reformatting input files - may need customisation of scripts for each dataset

$(DATADIR)/$(DATASET)/$(DATASET)_%_metadata.xml:
	touch $@

$(DATADIR)/$(DATASET)/$(DATASET)_tpm.tsv:
	touch $@

.PHONY: process_new_sample_xml
process_new_sample_xml: $(DATADIR)/$(DATASET)/$(DATASET)_sample_metadata.xml install_requirements
	python3 $(SCRIPTSDIR)/format_sample_data.py $(DATASET)

.PHONY: process_new_exp_tsv
process_new_exp_tsv: $(DATADIR)/$(DATASET)/$(DATASET)_tpm.tsv install_requirements
	python3 $(SCRIPTSDIR)/format_exp_data.py $(DATASET)

######## overwrite some ODK goals to prevent unnecessary processing

$(EDIT_PREPROCESSED): $(SRC)
	cp $< $@

$(SRCMERGED): $(EDIT_PREPROCESSED) $(OTHER_SRC)
	cp $< $@

$(PRESEED):
	touch $@

$(ALL_TERMS_COMBINED):
	touch $@

