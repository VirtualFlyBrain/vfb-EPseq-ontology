## Customize Makefile settings for VFB_EPseq
##
## If you need to customize your Makefile, make
## changes here rather than in the main Makefile

# uses aspects of scRNAseq pipeline, such as schema (extended here), but expected to be run one dataset at a time to make metadata and expression ontologies after some semi-automated pre-processing. Release process updates imports for all ontology files at once and produces all release files.

.PHONY: prepare_release_notest
# this prepares a release without updating the source files or running any tests
prepare_release_notest: all_imports release_ontology_files gen_docs $(REPORTDIR)/FBgn_list.txt
	rm -f $(CLEANFILES) $(ALL_TERMS_COMBINED) &&\
	echo "Release files are now in $(RELEASEDIR) - now you should commit, push and make a release on your git hosting site such as GitHub or GitLab"

########## directories and commands

DATADIR = ../data_files
EXPDIR = expression_data
METADATADIR = metadata_files
ONTOLOGYDIR = ontology_files
RELEASEDIR = ../../metadata_release_files
DATASET = PRJNA480794

$(EXPDIR) $(METADATADIR) $(RELEASEDIR) $(ONTOLOGYDIR):
	mkdir -p $@

LINKML = linkml-data2owl -s VFB_EPseq_schema.yaml
ROBOT_O = robot --catalog $(CATALOG_O)
CATALOG_O = $(ONTOLOGYDIR)/catalog-v001.xml

.PHONY: update_schema
update_schema:
	wget https://raw.githubusercontent.com/VirtualFlyBrain/vfb-scRNAseq-ontology/main/src/ontology/VFB_scRNAseq_schema.yaml -O VFB_scRNAseq_schema.yaml

.PHONY: setup_venv
setup_venv:
	apt-get update
	apt-get -y install python3.12-venv
	python3 -m venv my-venv

.PHONY: install_linkml
install_linkml: setup_venv
	my-venv/bin/pip install linkml-owl==v0.4.1

.PHONY: install_xml_tools
install_xml_tools: setup_venv
	my-venv/bin/pip install beautifulsoup4
	my-venv/bin/pip install lxml

.PHONY: install_vfbconnect
install_vfbconnect: setup_venv
	my-venv/bin/pip install vfb-connect


################## EXPRESSION FILES

# First make a correctly-formatted $(EXPDIR)/$(DATASET)_expression_FINAL.tsv)

.PHONY: process_expdata
# split expression data into chunked sample tsvs - RUN THIS FIRST
process_expdata: | $(EXPDIR) $(METADATADIR)
	my-venv/bin/python3 $(SCRIPTSDIR)/process_expression_data.py $(DATASET)

# gene expression owl files for datasets that have 'sample' expression data tsvs or ofns (names are dataset_PRJxxxxxxx_x-sample_SAMxxxxxxx_chunk_x)
DATASET_EXP_FILES = $(sort $(filter-out sample_%,$(subst -,.owl ,$(wildcard $(EXPDIR)/*.tsv))) $(filter-out sample_%,$(subst -,.owl ,$(wildcard $(EXPDIR)/*.ofn))))

.PHONY: make_expression_files
# make ofns from tsvs - RUN THIS SECOND
make_expression_files: $(DATASET_EXP_FILES)

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
$(EXPDIR)/VFB_EPseq_exp_%.owl: make_exp_ofns
	$(ROBOT) merge --inputs "$(EXPDIR)/dataset_$**.ofn" \
	annotate --ontology-iri "http://purl.obolibrary.org/obo/VFB_EPseq/$@" \
	-o $(TMPDIR)/$*-exp-tmp.ofn &&\
	cat $(TMPDIR)/$*-exp-tmp.ofn | sed -e 's/(neo_custom:expression_\([a-z]\+\) "\([0-9]\+\.[0-9]\+\)")/(neo_custom:expression_\1 "\2"^^xsd:float)/g' -e 's/(neo_custom:hide_in_terminfo "\([a-z]\+\)")/(neo_custom:hide_in_terminfo "\1"^^xsd:boolean)/g' > $@ &&\
	$(ROBOT) convert -i $@ --format owl -o $@ &&\
	$(ROBOT) convert -i $@ --format owl -o $@.gz &&\
	rm -f $(wildcard $(EXPDIR)/dataset_$**.ofn) $(TMPDIR)/$*-exp-tmp.ofn

################### metadata file

# build metadata ontology for dataset
$(ONTOLOGYDIR)/VFB_EPseq_$(DATASET).owl: install_linkml update_schema | $(TMPDIR)
	$(LINKML) -C ExpressionPattern $(DATADIR)/$(DATASET)/$(DATASET)_sample_metadata_FINAL.tsv -o $(ONTOLOGYDIR)/$(DATASET)_sample_metadata.ofn &&\
	$(LINKML) -C DatasetEP $(DATADIR)/$(DATASET)/$(DATASET)_dataset_metadata_FINAL.tsv -o $(ONTOLOGYDIR)/$(DATASET)_dataset_data.ofn &&\
	my-venv/bin/python3 $(SCRIPTSDIR)/ontology_file_headers.py $(DATASET) &&\
	$(ROBOT) merge \
	--input $(ONTOLOGYDIR)/$(DATASET)_header.ofn \
	--input $(ONTOLOGYDIR)/$(DATASET)_sample_metadata.ofn \
	--input $(ONTOLOGYDIR)/$(DATASET)_dataset_data.ofn \
	--include-annotations true --collapse-import-closure false \
	convert --format owl \
	-o $@ &&\
	rm $(ONTOLOGYDIR)/$(DATASET)_sample_metadata.ofn $(ONTOLOGYDIR)/$(DATASET)_dataset_data.ofn $(ONTOLOGYDIR)/$(DATASET)_header.ofn


########## release steps - imports, merged and compressed release files, reports

# variables - need ontologies to be made already
# dataset IDs from ontologies in ontology_files
RELEASE_DATASETS = $(patsubst $(ONTOLOGYDIR)/VFB_EPseq_%.owl,%,$(wildcard $(ONTOLOGYDIR)/*.owl))
ONTOLOGY_IMPORT_FILES = $(patsubst %,$(IMPORTDIR)/%_import.owl,$(RELEASE_DATASETS))
IMPORT_SEED_FILES = $(patsubst %,$(IMPORTDIR)/%_terms.txt,$(RELEASE_DATASETS))
RELEASE_ONTOLOGY_FILES = $(patsubst %,$(RELEASEDIR)/VFB_EPseq_%.owl,$(RELEASE_DATASETS))

.PHONY: all_imports
all_imports: create_import_stubs $(ONTOLOGY_IMPORT_FILES) # merged import is default prerequisite
	rm -f $(IMPORTDIR)/*terms.txt $(IMPORTDIR)/*terms_combined.txt

.PHONY: create_import_stubs
# make an empty ontology for imports to stop robot complaining
create_import_stubs:
	for FILE in $(ONTOLOGY_IMPORT_FILES); do \
		if ! test -f $$FILE; then \
			cp $(IMPORTDIR)/empty_import.txt $$FILE &&\
			$(ROBOT) annotate -i $$FILE \
			--ontology-iri "http://purl.obolibrary.org/obo/VFB_EPseq/$$FILE" \
			-o $$FILE; fi; \
		done

# import seeds for each ontology
# need to add RO_0002292 (expresses), which is only in the expression imports
$(IMPORTDIR)/%_terms.txt: create_import_stubs | $(ONTOLOGYDIR) $(TMPDIR)
ifeq ($(IMP),true)
	$(ROBOT_O) query --input $(ONTOLOGYDIR)/VFB_EPseq_$*.owl --query ../sparql/external_terms.sparql $@ &&\
	echo "http://purl.obolibrary.org/obo/RO_0002292" >> $@
else
	touch $@
endif

$(IMPORTDIR)/merged_terms_combined.txt: $(IMPORT_SEED_FILES) | $(TMPDIR)
ifeq ($(IMP),true)
	cat $(IMPORT_SEED_FILES) | sort | uniq > $@
else
	touch $@
endif

.PHONY: update_catalog_files
update_catalog_files: install_xml_tools
	my-venv/bin/python3 $(SCRIPTSDIR)/update_catalogs.py

.PHONY: release_ontology_files
release_ontology_files: $(RELEASE_ONTOLOGY_FILES)
	echo $@

# create merged release files (no need to reason etc)
# remove expression import (loaded separately into VFB)
$(RELEASEDIR)/VFB_EPseq_%.owl: | $(RELEASEDIR)
	cat $(ONTOLOGYDIR)/VFB_EPseq_$*.owl | grep -v "http://purl.obolibrary.org/obo/VFB_EPseq/expression_data/" > $(ONTOLOGYDIR)/VFB_EPseq_$*-tmp.owl
	$(ROBOT_O) merge -i $(ONTOLOGYDIR)/VFB_EPseq_$*-tmp.owl \
	convert --format owl \
	-o $@ &&\
	rm -f $(ONTOLOGYDIR)/VFB_EPseq_$*-tmp.owl

# this is needed for gene annotations in vfb-scRNAseq-gene-annotations repo
$(REPORTDIR)/FBgn_list.txt: $(TMPDIR)/existing_FBgns.txt | $(REPORTDIR)
	cp $< $@ &&\
	rm -f $(EXPDIR)/*.fbgns.tmp

# make a $(SRC) file that imports all the owl files in ontology_files
$(SRC): setup_venv
	my-venv/bin/python3 $(SCRIPTSDIR)/ontology_file_headers.py src

# remove any existing docs and generate fresh
.PHONY: gen_docs
gen_docs: install_linkml
	rm -fr ../../docs
	gen-doc ./VFB_EPseq_schema.yaml --directory ../../docs

######## UPDATE OBSOLETE GENES

.PHONY: unzip_exp_files
# unzip expression files - overwrites any existing owl files, keeping .gz version too
unzip_exp_files:
	for FILE in $(EXPDIR)/*.owl.gz; \
	do gzip -dkf $$FILE; done

.PHONY: zip_exp_files
# zip expression files - overwrites any existing owl.gz files, keeping unzipped version too
zip_exp_files:
	for FILE in $(EXPDIR)/*.owl; \
	do $(ROBOT) convert -i $$FILE --format owl -o $$FILE.gz; done

# generating seed file (to extract FBgns from there) needs too much memory (so using grep)
$(TMPDIR)/existing_FBgns.txt: unzip_exp_files
	for FILE in $(EXPDIR)/*.owl; \
	do cat $$FILE | grep --only-matching -E "FBgn[0-9]+" | sort | uniq > $$FILE.fbgns.tmp; done &&\
	cat $(EXPDIR)/*.fbgns.tmp | sort | uniq > $@

.PHONY: get_gene_id_map
get_gene_id_map: install_postgresql
	# this won't work until https://flybase.github.io/docs/chado/functions#update_ids is fixed
	my-venv/bin/python3 $(SCRIPTSDIR)/print_id_query.py &&\
	psql -h chado.flybase.org -U flybase flybase -f ../sql/id_update_query.sql \
	 > $(TMPDIR)/id_validation_table.tsv

replace_gene_ids_in_files: $(TMPDIR)/existing_FBgns.txt
	# need to get 'tmp/id_validation_table.txt' file from manual use of id validator
	my-venv/bin/python3 $(SCRIPTSDIR)/update_FBgns_in_files.py &&\
	for FILE in $(EXPDIR)/*.owl; \
	do if [ -f $$FILE-processed.txt ]; \
	then mv $$FILE-processed.txt $$FILE \
	$(ROBOT) convert -i $$FILE --format owl -o $$FILE.gz; fi &&\
	rm -f $$FILE.fbgns.tmp; done
	
################# reformatting input files - may need customisation of scripts for each dataset

$(DATADIR)/$(DATASET)/$(DATASET)_%_metadata.xml:
	touch $@

$(DATADIR)/$(DATASET)/$(DATASET)_tpm.tsv:
	touch $@

.PHONY: process_new_sample_xml
process_new_sample_xml: $(DATADIR)/$(DATASET)/$(DATASET)_sample_metadata.xml install_xml_tools install_vfbconnect
	my-venv/bin/python3 $(SCRIPTSDIR)/format_sample_data.py $(DATASET)

.PHONY: process_new_exp_tsv
process_new_exp_tsv: $(DATADIR)/$(DATASET)/$(DATASET)_tpm.tsv
	my-venv/bin/python3 $(SCRIPTSDIR)/format_exp_data.py $(DATASET)

######## overwrite some ODK goals to prevent unnecessary processing

$(EDIT_PREPROCESSED): $(SRC)
	cp $< $@

$(SRCMERGED): $(EDIT_PREPROCESSED) $(OTHER_SRC)
	cp $< $@

$(PRESEED):
	touch $@

$(ALL_TERMS_COMBINED):
	touch $@
