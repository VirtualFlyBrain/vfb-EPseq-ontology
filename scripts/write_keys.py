#!/usr/bin/env python
"""Write projects/<p>/id_keys.tsv: the entities that need VFBseq ids.

Ids are minted in vfb-scRNAseq's registry so they are unique across both repos. With
a vfb-scRNAseq clone next to this one, on a branch there:

    uv run python scripts/mint_external_ids.py \\
        --keys ../vfb-EPseq-ontology/projects/<p>/id_keys.tsv \\
        --out  ../vfb-EPseq-ontology/projects/<p>/ids.tsv

then open a PR there for the registry change and commit ids.tsv here.

`--check` fails instead if id_keys.tsv is out of date (a sample or driver changed at
GEO, or a config change) or any key has no id in ids.tsv.

Usage: uv run python scripts/write_keys.py --project davis_2020 [--check]
"""
import argparse
import sys
import tempfile
from pathlib import Path

import _common  # noqa: F401
from vfb_epseq.build import keys, read_ids, read_tpm, write_keys
from vfb_epseq.project import geo_series, load_config, needs_table, select_samples, tpm_path

ap = argparse.ArgumentParser()
ap.add_argument("--project", required=True)
ap.add_argument("--check", action="store_true")
args = ap.parse_args()
cfg = load_config(args.project)
samples, _ = select_samples(geo_series(cfg), cfg, read_tpm(cfg, tpm_path(cfg)) if needs_table(cfg) else None)
rows = keys(cfg, samples)
out = cfg["_dir"] / "id_keys.tsv"
if args.check:
    with tempfile.TemporaryDirectory() as tmp:
        write_keys(Path(tmp) / "k.tsv", rows)
        if (Path(tmp) / "k.tsv").read_text() != out.read_text():
            sys.exit(f"{out.name} is out of date: run scripts/write_keys.py and mint any new ids")
    ids = read_ids(cfg["_dir"] / "ids.tsv")
    missing = [r["natural_key"] for r in rows if (r["entity_type"], r["natural_key"]) not in ids]
    if missing:
        sys.exit(f"keys with no id in ids.tsv (mint them): {missing}")
    print(f"{out.name} up to date ({len(rows)} keys, all with ids)")
else:
    write_keys(out, rows)
    print(f"wrote {out} ({len(rows)} keys)")
