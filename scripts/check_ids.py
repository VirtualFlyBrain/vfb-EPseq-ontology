#!/usr/bin/env python
"""Check projects/*/ids.tsv against vfb-scRNAseq's id registry (main by default).

Every id here must be registered there under the same entity type and natural key,
so the two repos never issue the same id twice.

Usage: uv run python scripts/check_ids.py [--registry path/to/registry.json]
"""
import argparse
import json
import sys
import urllib.request
from pathlib import Path

import _common  # noqa: F401
from vfb_epseq.build import read_ids
from vfb_epseq.project import REPO_ROOT

URL = "https://raw.githubusercontent.com/VirtualFlyBrain/vfb-scRNAseq/main/id_registry/registry.json"

ap = argparse.ArgumentParser()
ap.add_argument("--registry", type=Path)
args = ap.parse_args()
if args.registry:
    reg = json.loads(args.registry.read_text())
else:
    with urllib.request.urlopen(URL, timeout=120) as r:  # noqa: S310
        reg = json.load(r)
entries = reg["entries"]
bad = []
files = sorted(REPO_ROOT.glob("projects/*/ids.tsv"))
for f in files:
    for (etype, key), vid in read_ids(f).items():
        e = entries.get(f"{etype}::{key}")
        if not e or e["id"] != vid:
            bad.append(f"{f.parent.name}: {etype} {key} -> {vid} (registry: {e['id'] if e else 'missing'})")
if bad:
    sys.exit("ids not matching vfb-scRNAseq's registry:\n  " + "\n  ".join(bad))
print(f"ids ok ({len(files)} project(s))")
