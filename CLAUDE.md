# vfb-EPseq-ontology

RDF/OWL for driver-sorted (expression pattern) RNA-seq datasets, for Virtual Fly Brain.
Read `README.md`, then `docs/DESIGN.md`. Works like `../vfb-scRNAseq` (read its
CLAUDE.md and docs/DESIGN.md *General curation rules*), which it installs as a package.

- Environment: `uv`. Before committing: `uv run pytest`, `uv run python scripts/check_ids.py`,
  `uv run python scripts/write_keys.py --project <p> --check`.
- Shared code (schema, emit, gene ids, GEO ingest) lives in vfb-scRNAseq: change it
  there, then bump the pinned `rev` in `pyproject.toml` (`uv lock`). EPseq-only schema
  goes in `schema/VFB_EPseq_schema.yaml` (an extension importing `vfb_scrnaseq`), never
  in the master schema.
- Dataset knowledge lives in `projects/<name>/config.yaml` and `drivers.tsv`; `src/` and
  `scripts/` stay dataset-agnostic.
- Ids: `VFBseq_` ids are minted only in vfb-scRNAseq's registry
  (`scripts/mint_external_ids.py` there, from this repo's `id_keys.tsv`), in a PR there;
  commit the returned `ids.tsv` here. Accessions are xrefs, never IRIs.
- Inputs (GEO SOFT, TPM tables) go in `.cache/` (gitignored), never in git.
- Commit on a branch and open a PR; show the PR text to the curator first.
