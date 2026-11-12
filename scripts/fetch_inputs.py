#!/usr/bin/env python
"""Download a project's inputs into .cache/: the GEO SOFT file and the TPM table.

Usage: uv run python scripts/fetch_inputs.py --project davis_2020
"""
import argparse

import _common  # noqa: F401
from vfb_epseq.build import read_tpm
from vfb_epseq.project import geo_series, load_config, needs_table, select_samples, tpm_path

ap = argparse.ArgumentParser()
ap.add_argument("--project", required=True)
args = ap.parse_args()
cfg = load_config(args.project)
series = geo_series(cfg)
keep, left_out = select_samples(series, cfg, read_tpm(cfg, tpm_path(cfg)) if needs_table(cfg) else None)
print(f"{series.accession}: {len(series.samples)} GEO samples, {len(keep)} loaded, {len(left_out)} left out")
print(f"TPM table: {tpm_path(cfg)}")
