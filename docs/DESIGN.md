# Design

## Relation to vfb-scRNAseq

Migrated in place from an ODK repo in November 2026 (one dataset, so no new repo).
vfb-scRNAseq is a uv git dependency, pinned to a commit, for:

- **Schema:** `schema/VFB_EPseq_schema.yaml` imports the master schema as `vfb_scrnaseq`
  (resolved to the installed package) and adds `EPseqDataset` (Dataset + Expression
  Atlas xref), `DriverSample` (Sample + `expression_pattern`, GEO and BioSample xrefs)
  and its container. `vfb_scrnaseq.emit` validates and emits with it.
- **Gene ids:** `vfb_scrnaseq.gene_ids` (FlyBase Chado), same statuses and rules as
  vfb-scRNAseq.
- **GEO:** `vfb_scrnaseq.ingest` reads the series SOFT file (sample titles,
  characteristics, BioSample and SRA relations).
- **Ids:** minted in vfb-scRNAseq's `id_registry/registry.json` via its
  `scripts/mint_external_ids.py`, so the two repos never issue the same id. Natural keys
  follow its form: `<GEO series>` for the Dataset, `<GEO series>:<sample title>` for a
  Sample. CI checks `ids.tsv` against the registry on vfb-scRNAseq main.

**Ids are not final until published on the live VFB site** (virtualflybrain.org). Until
an entity is in a VFB release, anything about it may change: re-keyed, re-minted or
dropped, with its config, mappings and output files. Once it is live its id is fixed.

Before the migration, samples and the dataset had NCBI BioSample / BioProject IRIs
(`http://www.ncbi.nlm.nih.gov/biosample/SAMN...`); these are now xrefs.

## Publishing (todo, when ready to load)

Output files are named by project (`<author>_<year>`), as in vfb-scRNAseq (2026-11-11;
previously by BioProject). VFB still loads the previous release files, under the old names,
from the legacy Jenkins job (`metadata_release_files/`, `src/ontology/`). When the Argo
publish job replaces it, apply the renames there and in collectdata together, before the
next data release:

- **Argo publish job** (vfb-k8s, like `scrnaseq-publish` with vfb-scRNAseq's
  `scripts/release_files.py`): publish `metadata/vfb_EPseq_metadata_<project>.owl` as
  `VFB_EPseq_metadata_<project>.owl`, and `expression/vfb_EPseq_expression_<project>_<n>.owl.gz`
  unzipped as `VFB_EPseq_exp_<project>_<n>.owl`. Remove the old `VFB_EPseq_PRJNA480794.owl`
  and `VFB_EPseq_exp_PRJNA480794_*.owl` from the OWL dir, or Davis loads twice.
- **collectdata** (`vfb-pipeline-collectdata`, `vfb_fullontologies.txt`): `VFB_EPseq_PR*`
  -> `VFB_EPseq_metadata_*` (and the README examples). Change it with the first publish:
  the old glob matches none of the new files, the new one none of the old.
- **Unchanged:** the dumps `PDB_EXTERNAL_ONTS` and vfb-data-release globs
  (`VFB_EPseq_exp_*.owl`) match the new expression names.
- **vfb-scRNAseq-gene-annotations:** read `expression/FBgn_list.txt` (not
  `src/ontology/reports/FBgn_list.txt`).

## Model

- **Dataset** (FBcv:0003023): label `<method> data from <Author> (<year>)` (`Bulk RNA-seq`
  from Aso 2019 on; the isolation method goes in the description), optional assay type
  (`dataset.assay_type`, e.g. FBcv:0009018 *cell type-specific RNA-sequencing analysis*), description,
  publication, licence, GEO and Expression Atlas xrefs. Node label `DataSet`.
- **Sample** (FBcv:0003024): one per driver-sorted GEO sample, label `<sample title>
  (<Author> <year>)`. Instance of the driver's `VFBexp_` expression pattern class (VFB
  links the sample to the driver through it); overlaps the dissected tissue; stage; the
  dataset (`dc:source`); GEO (GSM) and BioSample xrefs. Where the authors give the cell
  type their driver labels, the sample is *composed primarily of* (RO:0002473) it, as a
  Cluster is in vfb-scRNAseq (`cell_types.tsv`: author type -> FBbt).
- **Expression:** `expresses` (RO:0002292) a gene, annotated with `expression_level`
  (the authors' TPM) and `hide_in_terminfo` true. No extent (bulk RNA-seq).

Not yet modelled (todo): Assays (the SRA runs), `genotype_includes` (the FBco / FBtp
of each driver and the UAS reporter), an assay type for TAPIN-seq / INTACT, and the 8
dissected lamina / optic lobe samples as tissue samples (FBbt tissue, no expression
pattern class).

## Drivers and cell types (all projects)

- **Driver -> VFBexp class** (`drivers.tsv`, keyed by the GEO characteristic
  `samples.driver_field`). A split line can match several VFBexp classes: the same AD in
  attP40 (`P{}`) and VK00027 (`PBac{}`), FBcos with the halves swapped, or later combined
  constructs. Take the line's AD and DBD insertions from Janelia's combinations file
  (`flylight-split-gal4-curation` `data/flylight_combination_lines_VFB.tsv`) and check them
  against the line name (Aso 2014a: DBD in attP2; AD in su(Hw)attP8 / attP40 / VK00027 for
  suffix A / B / C); record AD, DBD and evidence per line. Look classes up by FBtp pair,
  not by line name: a class may carry only another line's name (lines sharing an AD+DBD
  pair are one class). A driver not in the table stops the build; one with no class
  (e.g. a GAL4 restricted by FLP, which has no intersection class) leaves its samples out.
- **Classic GAL4 lines** (named loosely, e.g. `TH-GAL4`): take the construct or
  insertion from FlyBase's curation of the paper where it lists one per driver, else the
  paper's cited source; never a guess from the name alone.
- **No narrower type** (a pan-neuronal driver such as elav-GAL4, or a line whose cells are
  mixed neurons): *adult neuron* (FBbt:00047095) where the cells are known to be neurons.
  Unlike an scRNAseq cluster (held when typeable only as *neuron*), the sample still has its
  driver, so the generic class adds to it (curator 2026-11-12). Untyped only where even
  that isn't stated (Davis Kdm2).
- **Pooled GEO samples** (`samples.libraries`): a GEO sample that pools several libraries,
  each with its own column, line and cell type in the authors' table, gives one Sample per
  library (natural key `<GEO series>:<sample title>:<library>`; the GSM and BioSample are
  shared xrefs). Values are never combined across libraries.
- **Expression values:** the authors' gene-level values only. A dataset with only
  transcript- or exon-level values is not loaded (curator 2026-11-12: e.g. Abruzzi 2017,
  ESAT per-transcript values where isoforms sharing a 3' end get the same reads); summing
  transcripts is fine only where each read is assigned once (RSEM, Salmon), as the authors'
  own gene value. Counts with no normalised values are scaled to counts per million
  (`expression.normalise: cpm`, as for scRNAseq), over the sample's FBgn rows.
- **Cell types** (optional `cell_types.tsv`): the authors' type for each sample, matched
  from the title by `samples.cell_type_pattern`, mapped to one FBbt term (the common
  parent where the driver labels several types, as for a grouped cluster call in
  vfb-scRNAseq). Several terms are fine where each applies to most of the cells and
  they don't contradict one another, e.g. a type and its lineage or neurotransmitter
  class; never sibling types that each hold only part of the sample (two *composed
  primarily of* types that split the cells contradict each other). Typed from the
  driver as the authors state it, never from
  our reading of the expression. An author type not in the table stops the build.

## Davis 2020 (`davis_2020`)

GEO GSE116969 (BioProject PRJNA480794, Expression Atlas E-GEOD-116969), FBrf0244935,
CC BY 4.0. 266 GEO samples; 238 loaded. Inputs: the SOFT file and supplementary
`dataTable2.genes_x_samples_TPM.all_genes` (identical to the TPM table of the 2024
curation).

- **Method:** TAPIN-seq / INTACT: nuclei affinity-purified (anti-GFP beads) from
  homogenised frozen heads by the driver's tagged nuclear envelope protein (UNC84-GFP);
  no cell sorting. Dataset label *Bulk RNA-seq data from Davis (2020)* (method in the
  title), assay type FBcv:0009018.
- **Tissue / stage:** whole heads (GEO `tissue: head`), adult (FBdv:00005369), except
  Muscles_App (2 samples): *appendage* (FBbt:00007000; `samples.tissue_by_cell_type`).
  GEO gives head for every sample, but the paper says these libraries were made from
  appendages after the heads were removed (Figure 3 - figure supplement 1 legend; table A;
  methods "heads or wings/appendages").
- **Cell types** (`cell_types.tsv`, 2026-11-11): the authors' type is the title before
  `_d<n>` (supplementary table A `celltype`, with `celltype.details`). Combination and
  multi-type drivers (C2.C3, L1.L2, T4.T5, KC α/β c.p.s, LPTC HS.VS, LC10bc, PB_1, PAM_2/3/4/6)
  map to the common parent; broad drivers (putative ChAT-, Gad1-, VGlut-, CCAP-, Crz-,
  Dsk-, Ilp2-, NPF-, Pdf-expressing cells) to the adult neurotransmitter / peptide class.
  PB_3 (P-EN1 driver, but the authors note optic lobe cells outnumber the PB cells) ->
  *adult neuron* (2026-11-12). No type: Kdm2 (broad enhancer trap; the authors don't say
  which cells, so not even *neuron*). 236 of 238 samples typed.
- **Drivers:** `drivers.tsv` maps GEO's `external driver id` to a `VFBexp_` class, from
  the 2024 curation (VFB lookup by name; 14 matched by hand). GEO gives `JSS55439` for
  the Glia_Eg samples where BioSample gives `SS55439`; both are listed. A driver id not
  in the table stops the build.
- **Left out** (`projects/davis_2020/samples_left_out.tsv`): 16 TAPIN controls; 8 lamina /
  optic lobe dissections (SS00796, SS55439: bulk RNA from dissected tissue, GEO protocol
`bulk` with no reporter, so not captured by the driver and not instances of its
expression pattern; left out in 2024 too); 4
  R1-6 samples (ninaE driver FBtp0092375 has no VFBexp class; checked 2026-11-10).
- **Gene ids** (`gene_id_map.tsv`, FB2026_03): retired ids replaced by their current
  gene; 3 split ids (CG30456, Osi10, Iyd) and 1 withdrawn id (FBgn0003926) dropped; ERCC
  spike-ins skipped. Where several input ids now belong to one gene (FlyBase merges):
  rows identical in all 266 samples (CG30497 / CG45093, CG11566 / stg1: overlapping
  models given the same reads) count once; genes whose input rows differ (xmas from
  xmas-1 / xmas-2, Or67c from CR44541 / Or67c, lncRNA:CR46499 from CG12688 / CR45484)
  are dropped, since the overlap between the old models, and so the TPM of the merged
  gene, is unknown.

### Differences from the 2025 release (checked 2026-11-10)

Same 238 driver-typed samples with the same drivers, tissue, stage and dataset links.

- New `VFBseq_` IRIs (VFBseq_00003283-00003521); BioSample and GEO xrefs added on
  samples; new labels `Bulk RNA-seq data from Davis (2020)` and `Mi1_d1_rep1 (Davis
  2020)`, previously `RNAseq_2020_Davis` and `RNAseq_2020_DavisMi1_d1_rep1`.
- Added since: assay type and sample cell types (2026-11-11).
- The 4 R1-6 samples (no driver class, no expression) are no longer loaded.
- Expression: 2,717,993 axioms (was 2,718,789). Iyd (FBgn0286980, 206 axioms) dropped
  as a split (the 2024 curation mapped it by name); 3 merged genes with differing input
  rows dropped (xmas, Or67c, lncRNA:CR46499; 590 axioms); 5 genes renamed by FlyBase
  since 2025-10 moved to their new ids; all other values identical.

## Aso 2019 (`aso_2019`; ids minted, not yet released)

GEO GSE139889 (BioProject PRJNA587485), FBrf0244530, CC BY 4.0. 55 GEO samples; 50
loaded. Cells hand-picked or FACS-sorted (GEO `sorting`, per sample) from dissociated
adult female brains, by split-GAL4 (Aso 2014a) or GAL4 driving a fluorescent reporter.

- **Tissue / stage:** adult brain (FBbt:00003624; paper methods, GEO has no tissue),
  adult. Dataset label *Bulk RNA-seq data from Aso (2019)*, assay type FBcv:0009018.
- **Drivers / cell types:** `drivers.tsv` (AD / DBD and evidence per line) and
  `cell_types.tsv` (author type from the title). Lines labelling several sibling types
  map to the common parent (MBON-α′3, PAM-β1/β2, PAM-γ4<γ1γ2 + PAM-γ4).
- **Left out:** the 5 APL samples (NP2631-GH146-flp: GAL4 restricted by FLP, no
  intersection class).
- **Expression:** supplementary file 1 (xlsx, RSEM transcript TPM on r6.34): transcript
  TPM summed per gene; columns matched to samples by PID (the title prefix); 99 rows with
  no FBgn (non-FlyBase sequences, GAL4 / LexA transgenes) skipped, as Davis's ERCCs, so
  gene TPMs are not renormalised.
- **Gene ids** (FB2026_03): 17,612 genes; 74 retired ids replaced, 1 withdrawn
  (snRNA:U3) dropped, no splits. Merged genes are summed (`merged_genes: sum`): RSEM
  assigns each read once across transcripts, so the sum is the merged gene's TPM. stg1's
  two old models (CG11566 / stg1) have identical TPMs in every sample, as in Davis; under
  EM that is reads split evenly between indistinguishable transcripts, not duplicated.
- Build: 51 entities (VFBseq_00003522-00003572), 381,696 expression axioms, 15,237
  genes, 2,863-11,087 genes per sample. Not in a VFB release yet (that waits for the
  Argo job replacing Jenkins), so still open to change.

## Schretter 2020 (`schretter_2020`; ids minted, not yet released)

GEO GSE158748 (BioProject PRJNA666415), FBrf0247707, eLife, CC BY 4.0. Same Janelia
pipeline as Aso 2019. 6 GEO samples; 20 loaded.

- **Tissue / stage:** adult brain (60-100 dissected per sample; GEO extract protocol), adult
  females. Dataset label *Bulk RNA-seq data from Schretter (2020)*, assay type FBcv:0009018.
- **Samples:** 5 bulk samples of 400-800 FACS-sorted cells (two aIPg lines). GSM4809508
  (`pC1d_pC1de_pC1e_RNAseq_reps`) pools 15 low-cell libraries of ~40 hand- or FACS-sorted
  cells from 4 lines; the spreadsheet gives each library a column (`<plate>_<well>_Sample_Rubin_DGE_pool01`),
  line and cell type, so each is a Sample (`samples.libraries`; curator 2026-11-12). Bulk
  samples' columns are their GEO descriptions (`expression.sample_columns`).
- **Drivers / cell types:** 6 split-GAL4 lines; AD / DBD from Janelia's combinations file,
  matching the paper's key resources table. aIPg lines label several aIPg types (parent
  FBbt:00052698); SS43274 labels pC1d and pC1e (parent *adult doublesex pC1 (female) neuron*).
- **Expression:** supplementary file 1 (xlsx, r6.34): gene counts only (RSEM expected counts
  for bulk, STARsolo UMI counts for low-cell), scaled to CPM over each sample's FBgn rows
  (curator 2026-11-12); ERCC spike-ins and transgene rows skipped. Gene ids as Aso (FB2026_03:
  74 retired ids replaced, snRNA:U3 dropped, 3 merges summed: RSEM and STARsolo assign each
  read / UMI once).
- Build: 21 entities (VFBseq_00003573-00003593), 124,700 expression axioms, 13,725 genes.
  `FBgn_list.txt` grows by 85 genes (16,948 -> 17,033).

## Sapiro 2019 (`sapiro_2019`; ids minted, not yet released)

GEO GSE113661 (BioProject PRJNA453551; SubSeries of GSE113663), FBrf0241444, PNAS, CC BY 4.0.
30 GEO samples; 27 loaded.

- **Method / tissue / stage:** INTACT (UNC84-2xGFP nuclei affinity-purified from ~300
  homogenised heads), 10 GAL4 lines x 3 replicates; adult head (FBbt:00000004), adult (2-3 day).
- **Drivers:** GEO `genotype` (`UAS-unc84-2XGFP; <name>-GAL4`). Each line from FlyBase's
  curation of the paper (one GAL4 per driver), e.g. TH-GAL4 = P{ple-GAL4.F}, fru-GAL4 =
  TI{GAL4}fru[GAL4.P1.D], elav-GAL4 = P{GawB}elav[C155], Dh44-GAL4 = P{VT039046-GAL4}.
- **Left out:** the 3 NPFR samples (P{NPFR-GAL4.T}, FBtp0131830, is not in VFB, so no
  VFBexp class; checked 2026-11-12).
- **Cell types:** the authors' populations (`cell_types.tsv`): Dh44 -> *adult Dh44 neuron of
  brain* (heads), Tdc2 -> *adult octopaminergic neuron* as the authors name it, OK107 ->
  *adult Kenyon cell*, fru -> *fruitless expressing neuron*; elav (pan-neuronal reference)
  -> *adult neuron*.
- **Expression:** GEO RAW.tar, per-sample featureCounts gene counts keyed by gene name
  (`-g gene_name`) in Ensembl BDGP6.88, mapped to FBgn through that GTF (each name is one
  gene there); the `*_RNAseq_editing` files are editing levels and are skipped. Raw counts
  only, scaled to CPM. Gene ids (FB2026_03): 17,490 genes; 254 retired ids replaced, 9 split
  and 1 withdrawn dropped, 11 merges summed (featureCounts counts each read once).
- Build: 28 entities (VFBseq_00003594-00003621), 344,353 expression axioms, 16,386 genes.
