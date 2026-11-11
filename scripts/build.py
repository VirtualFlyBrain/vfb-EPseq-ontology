#!/usr/bin/env python
"""Build a project's OWL: metadata/VFB_EPseq_<name>.owl and
expression/VFB_EPseq_exp_<name>_<n>.owl.gz, plus expression/FBgn_list.txt (every gene
in the expression output, read by vfb-scRNAseq-gene-annotations) and
projects/<p>/samples_left_out.tsv.

Needs the inputs in .cache/ (fetched if missing), ids.tsv and gene_id_map.tsv, and
ROBOT on PATH for the OWL/XML conversion.

Usage: uv run python scripts/build.py --project davis_2020 [--metadata-only]
"""
import argparse
import csv
import re
import tempfile
from pathlib import Path

import _common  # noqa: F401
from vfb_scrnaseq.emit import emit_expression_owl, emit_owl, to_owlxml
from vfb_epseq.build import IdLookup, entities, expression, gene_map, read_ids, read_tpm
from vfb_epseq.project import REPO_ROOT, SCHEMA, geo_series, load_config, select_samples, tpm_path

ap = argparse.ArgumentParser()
ap.add_argument("--project", required=True)
ap.add_argument("--metadata-only", action="store_true")
args = ap.parse_args()

cfg = load_config(args.project)
name = cfg["dataset"]["output_name"]
samples, left_out = select_samples(geo_series(cfg), cfg)
ids = IdLookup(cfg, read_ids(cfg["_dir"] / "ids.tsv"))

with (cfg["_dir"] / "samples_left_out.tsv").open("w", newline="") as fh:
    w = csv.DictWriter(fh, fieldnames=["gsm", "title", "reason"], delimiter="\t", lineterminator="\n")
    w.writeheader()
    w.writerows(sorted(left_out, key=lambda r: r["gsm"]))

ents = entities(cfg, samples, ids)
(REPO_ROOT / "metadata").mkdir(exist_ok=True)
with tempfile.TemporaryDirectory() as tmp:
    ofn = emit_owl(ents, Path(tmp) / f"{name}.ofn", schema_path=SCHEMA)
    out = to_owlxml(ofn, REPO_ROOT / "metadata" / f"VFB_EPseq_{name}.owl")
print(f"{len(ents)} entities ({len(samples)} samples; {len(left_out)} left out) -> {out}")

if not args.metadata_only:
    exp_dir = REPO_ROOT / "expression"
    exp_dir.mkdir(exist_ok=True)
    for old in exp_dir.glob(f"VFB_EPseq_exp_{name}_*.owl.gz"):
        old.unlink()
    genes: set[str] = set()
    chunks = expression(cfg, read_tpm(cfg, tpm_path(cfg)), samples, ids, gene_map(cfg["_dir"] / "gene_id_map.tsv"))
    for n, rows in enumerate(chunks, 1):
        genes.update(r[2] for r in rows)
        out = emit_expression_owl(rows, exp_dir / f"VFB_EPseq_exp_{name}_{n}.owl.gz", schema_path=SCHEMA)
        print(f"{len(rows)} expression axioms -> {out}")
    fbgns = sorted(g for g in genes if re.fullmatch(r"FBgn\d+", g))
    (exp_dir / "FBgn_list.txt").write_text("".join(f"{g}\n" for g in fbgns))
    print(f"{len(fbgns)} genes -> {exp_dir / 'FBgn_list.txt'}")
