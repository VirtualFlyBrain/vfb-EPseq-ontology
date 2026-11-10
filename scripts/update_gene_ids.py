#!/usr/bin/env python
"""Map the TPM table's gene ids to current FlyBase genes -> projects/<p>/gene_id_map.tsv.

Uses vfb-scRNAseq's gene-id code (FlyBase Chado; needs `psql`): current ids are kept,
a retired id of one current gene is replaced by it, split / withdrawn / non-gene ids are
dropped. Where several ids merged into one gene, the build keeps it only if their rows
are identical. The build reads the committed map, so it needs no Chado access.

Usage: uv run python scripts/update_gene_ids.py --project davis_2020 [--release FB2026_03]
"""
import argparse
import sys

import _common  # noqa: F401
from vfb_scrnaseq import gene_ids
from vfb_epseq.build import tpm_features
from vfb_epseq.project import load_config, tpm_path

ap = argparse.ArgumentParser()
ap.add_argument("--project", required=True)
ap.add_argument("--release", default="", help="override the FlyBase release read from flybase.org")
args = ap.parse_args()
cfg = load_config(args.project)
release = args.release or gene_ids.flybase_release()
if not release:
    print("  WARNING: could not read the FlyBase release from flybase.org; pass --release", file=sys.stderr)
rows = gene_ids.reclassify(tpm_features(tpm_path(cfg)))
out = cfg["_dir"] / "gene_id_map.tsv"
counts = gene_ids.write_map(out, rows, release)
merges = counts.pop("merges")
print(f"wrote {out}: {counts}; merges: {merges}")
