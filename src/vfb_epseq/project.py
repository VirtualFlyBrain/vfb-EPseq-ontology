"""A project's config, inputs (GEO SOFT + TPM table, cached in .cache/) and samples.

All dataset-specific knowledge is in ``projects/<name>/config.yaml`` and
``projects/<name>/drivers.tsv``; this module stays dataset-agnostic.
"""

from __future__ import annotations

import csv
import gzip
import shutil
import urllib.request
from dataclasses import dataclass
from pathlib import Path

import yaml
from vfb_scrnaseq.ingest import GeoSeries, fetch_soft, parse_soft

REPO_ROOT = Path(__file__).resolve().parents[2]
CACHE = REPO_ROOT / ".cache"
SCHEMA = REPO_ROOT / "schema" / "VFB_EPseq_schema.yaml"
GEO_SUPPL = "https://ftp.ncbi.nlm.nih.gov/geo/series/{stub}nnn/{acc}/suppl/{file}"


def project_dir(project: str) -> Path:
    return REPO_ROOT / "projects" / project


def load_config(project: str) -> dict:
    cfg = yaml.safe_load((project_dir(project) / "config.yaml").read_text())
    cfg["_dir"] = project_dir(project)
    return cfg


def geo_series(cfg: dict) -> GeoSeries:
    """The GEO series (SOFT, full view), fetched once into .cache/."""
    acc = cfg["source"]["geo_series"]
    path = CACHE / f"{acc}_family.soft.gz"
    if not path.exists():
        CACHE.mkdir(exist_ok=True)
        text = fetch_soft(acc)
        with gzip.open(path, "wt") as fh:
            fh.write(text)
    with gzip.open(path, "rt") as fh:
        return parse_soft(fh.read())


def tpm_path(cfg: dict) -> Path:
    """The TPM table (GEO supplementary file), downloaded once into .cache/."""
    acc, name = cfg["source"]["geo_series"], cfg["expression"]["tpm_file"]
    path = CACHE / name
    if not path.exists():
        CACHE.mkdir(exist_ok=True)
        url = GEO_SUPPL.format(stub=acc[:-3], acc=acc, file=name)
        tmp = path.with_suffix(".part")
        with urllib.request.urlopen(url, timeout=300) as r, tmp.open("wb") as fh:  # noqa: S310
            shutil.copyfileobj(r, fh)
        tmp.rename(path)
    return path


def read_drivers(path: Path) -> dict[str, tuple[str, str]]:
    """drivers.tsv -> {GEO external driver id: (VFBexp class or '', note)}."""
    with path.open() as fh:
        rows = csv.DictReader((ln for ln in fh if not ln.startswith("#")), delimiter="\t")
        return {r["external_driver_id"]: (r["expression_pattern"], r["note"]) for r in rows}


@dataclass
class Sample:
    title: str            # the authors' sample name (GEO title; the TPM table's column)
    gsm: str
    biosample: str
    driver_id: str        # GEO "external driver id"
    expression_pattern: str


def select_samples(series: GeoSeries, cfg: dict) -> tuple[list[Sample], list[dict]]:
    """(samples to load, [{title, gsm, reason}] left out), in GEO order.

    Raises on a driver id missing from drivers.tsv (a new driver needs curating)."""
    sc = cfg["samples"]
    drivers = read_drivers(cfg["_dir"] / sc["drivers"])
    exclude = sc.get("exclude_driver_types", {})
    keep, left_out, missing = [], [], set()
    for s in series.samples:
        dtype = (s.characteristic("driver type") or "").strip()
        driver_id = (s.characteristic("external driver id") or "").strip()
        if dtype in exclude:
            left_out.append({"title": s.title, "gsm": s.accession, "reason": exclude[dtype].strip()})
            continue
        if driver_id not in drivers:
            missing.add(driver_id)
            continue
        vfbexp, note = drivers[driver_id]
        if not vfbexp:
            left_out.append({"title": s.title, "gsm": s.accession, "reason": note or "no VFBexp class"})
            continue
        keep.append(Sample(s.title, s.accession, s.relations.get("BioSample", ""), driver_id, vfbexp))
    if missing:
        raise ValueError(f"driver ids not in {sc['drivers']} (curate them): {sorted(missing)}")
    return keep, left_out
