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

## Datasets

| Project | Paper | Data | Samples | Drivers |
|---|---|---|---|---|
| `davis_2020` | Davis et al. 2020 (FBrf0244935), TAPIN-seq of adult optic lobe neurons | GEO GSE116969 / BioProject PRJNA480794 | 238 | 113 |

## Outputs

- `metadata/VFB_EPseq_<name>.owl`: the Dataset and Samples. Each Sample is typed by its
  driver's expression pattern class (`VFBexp_...`), with tissue, stage, dataset and xrefs.
- `expression/VFB_EPseq_exp_<name>_<n>.owl.gz`: per-sample gene expression (TPM as
  `expression_level`, `hide_in_terminfo` true), up to 100 samples per file.
- `expression/FBgn_list.txt`: every gene in the expression output (for
  vfb-scRNAseq-gene-annotations).

Until VFB publishes from these paths, the previous release files stay where the old
Jenkins job reads them: `metadata_release_files/`, `src/ontology/expression_data/`,
`src/ontology/reports/FBgn_list.txt`.

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
