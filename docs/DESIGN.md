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

Before the migration, samples and the dataset had NCBI BioSample / BioProject IRIs
(`http://www.ncbi.nlm.nih.gov/biosample/SAMN...`); these are now xrefs.

## Model

- **Dataset** (FBcv:0003023): label `<method> data from <Author> (<year>)`, description,
  publication, licence, GEO and Expression Atlas xrefs. Node label `DataSet`.
- **Sample** (FBcv:0003024): one per driver-sorted GEO sample, label `<sample title>
  (<Author> <year>)`. Instance of the driver's `VFBexp_` expression pattern class (VFB
  links the sample to the driver through it); overlaps the dissected tissue; stage; the
  dataset (`dc:source`); GEO (GSM) and BioSample xrefs.
- **Expression:** `expresses` (RO:0002292) a gene, annotated with `expression_level`
  (the authors' TPM) and `hide_in_terminfo` true. No extent (bulk RNA-seq).

Not yet modelled (todo): Assays (the SRA runs), `genotype_includes` (the FBco / FBtp
of each driver and the UAS reporter), an assay type for TAPIN-seq.

## Davis 2020 (`davis_2020`)

GEO GSE116969 (BioProject PRJNA480794, Expression Atlas E-GEOD-116969), FBrf0244935,
CC BY 4.0. 266 GEO samples; 238 loaded. Inputs: the SOFT file and supplementary
`dataTable2.genes_x_samples_TPM.all_genes` (identical to the TPM table of the 2024
curation).

- **Tissue / stage:** whole heads (GEO `tissue: head`), adult (FBdv:00005369).
- **Drivers:** `drivers.tsv` maps GEO's `external driver id` to a `VFBexp_` class, from
  the 2024 curation (VFB lookup by name; 14 matched by hand). GEO gives `JSS55439` for
  the Glia_Eg samples where BioSample gives `SS55439`; both are listed. A driver id not
  in the table stops the build.
- **Left out** (`projects/davis_2020/samples_left_out.tsv`): 16 TAPIN controls; 8 lamina /
  optic lobe dissections (SS00796, SS55439; left out in 2024, reason not recorded); 4
  R1-6 samples (ninaE driver FBtp0092375 has no VFBexp class; checked 2026-11-10).
- **Gene ids** (`gene_id_map.tsv`, FB2026_03): retired ids replaced by their current
  gene; 3 split ids (CG30456, Osi10, Iyd) and 1 withdrawn id (FBgn0003926) dropped; ERCC
  spike-ins skipped. Where several input ids now belong to one gene, TPM is summed,
  except that rows identical in all 266 samples (CG30497 / CG45093, CG11566 / stg1:
  overlapping models given the same reads) are counted once.

### Differences from the 2025 release (checked 2026-11-10)

Same 238 driver-typed samples with the same drivers, tissue, stage and dataset links.

- New `VFBseq_` IRIs (VFBseq_00003283-00003521); BioSample and GEO xrefs added on
  samples; new labels (`TAPIN-seq data from Davis (2020)`, `Mi1_d1_rep1 (Davis 2020)`;
  previously `RNAseq_2020_Davis`, `RNAseq_2020_DavisMi1_d1_rep1`).
- The 4 R1-6 samples (no driver class, no expression) are no longer loaded.
- Expression: 2,718,583 axioms (was 2,718,789). Iyd (FBgn0286980, 206 axioms) dropped
  as a split (the 2024 curation mapped it by name); 5 genes renamed by FlyBase since
  2025-10 moved to their new ids; 3 merged genes (xmas, Or67c, CR45484) now have the
  sum of their input ids' TPM; all other values identical.
