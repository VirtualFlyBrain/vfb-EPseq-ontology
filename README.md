![CI](https://github.com/VirtualFlyBrain/vfb-EPseq-ontology/actions/workflows/ci.yml/badge.svg)
# VFB expression-pattern RNA-seq (EPseq)

RDF/OWL metadata and expression for *Drosophila* RNA-seq of cells sorted by a driver's
expression pattern (e.g. split-GAL4 lines driving a nuclear tag), for loading into
[Virtual Fly Brain](https://virtualflybrain.org). Only driver-sorted samples are loaded
(not controls).

It works like [vfb-scRNAseq](https://github.com/VirtualFlyBrain/vfb-scRNAseq) and
installs that repo as a package for the shared parts: the LinkML schema (extended here),
OWL emission, FlyBase gene-id mapping and GEO ingest. Ids are `VFBseq_` ids from
vfb-scRNAseq's registry; GEO / BioSample / Expression Atlas accessions are xrefs.

**Ids are not final until published on the live VFB site** (virtualflybrain.org). Until
an entity is in a VFB release, anything about it may change: re-keyed, re-minted or
dropped, with its config, mappings and output files. Once it is live its id is fixed.

## Datasets

| Project | Paper | Data | Samples | Drivers |
|---|---|---|---|---|
| `davis_2020` | Davis et al. 2020 (FBrf0244935), bulk RNA-seq (TAPIN-seq / INTACT) of adult head cell types, mostly optic lobe neurons | GEO GSE116969 / BioProject PRJNA480794 | 238 | 113 |
| `aso_2019` (not yet released) | Aso et al. 2019 (FBrf0244530), bulk RNA-seq of sorted mushroom body cell types | GEO GSE139889 / BioProject PRJNA587485 | 50 | 19 |
| `schretter_2020` (not yet released) | Schretter et al. 2020 (FBrf0247707), bulk and low-cell RNA-seq of sorted aIPg and pC1 neurons | GEO GSE158748 / BioProject PRJNA666415 | 20 | 6 |
| `sapiro_2019` (not yet released) | Sapiro et al. 2019 (FBrf0241444), INTACT RNA-seq of nuclei from 10 GAL4-labelled neuronal populations | GEO GSE113661 / BioProject PRJNA453551 | 27 | 9 |

## Outputs

Named by project (`<author>_<year>`), as in vfb-scRNAseq:

- `metadata/vfb_EPseq_metadata_<project>.owl`: the Dataset and Samples. Each Sample is typed by its
  driver's expression pattern class (`VFBexp_...`), with tissue, stage, dataset and xrefs.
- `expression/vfb_EPseq_expression_<project>_<n>.owl.gz`: per-sample gene expression (TPM as
  `expression_level`, `hide_in_terminfo` true), up to 100 samples per file.
- `expression/FBgn_list_<project>.txt`: the genes in a project's expression output;
  `expression/FBgn_list.txt`: their union, every project's genes (for
  vfb-scRNAseq-gene-annotations).

Until VFB publishes from these paths, the previous release files stay where the old
Jenkins job reads them: `metadata_release_files/`, `src/ontology/expression_data/`,
`src/ontology/reports/FBgn_list.txt`. Publishing from here needs the renames in
docs/DESIGN.md *Publishing*.

## Building

Needs `uv`, ROBOT on `PATH`, and for gene ids `psql` (FlyBase Chado).

```sh
uv sync --extra dev
uv run python scripts/fetch_inputs.py    --project davis_2020   # GEO SOFT + TPM table -> .cache/
uv run python scripts/write_keys.py      --project davis_2020   # entities needing ids -> id_keys.tsv
#   mint new ids in vfb-scRNAseq (see scripts/write_keys.py), commit ids.tsv here
uv run python scripts/update_gene_ids.py --project davis_2020   # -> gene_id_map.tsv (Chado)
ROBOT_JAVA_ARGS=-Xmx12g uv run python scripts/build.py --project davis_2020
uv run pytest
```

See [docs/DESIGN.md](docs/DESIGN.md) for the curation decisions.

## Contact

Please use this repository's [issue tracker](https://github.com/VirtualFlyBrain/vfb-EPseq-ontology/issues).
