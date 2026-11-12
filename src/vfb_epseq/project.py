"""A project's config, inputs (GEO SOFT + TPM table, cached in .cache/) and samples.

All dataset-specific knowledge is in ``projects/<name>/config.yaml``,
``projects/<name>/drivers.tsv`` and (optionally) ``cell_types.tsv``; this module stays
dataset-agnostic.
"""

from __future__ import annotations

import csv
import gzip
import re
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


def _read_tsv(path: Path) -> list[dict]:
    with path.open() as fh:
        return list(csv.DictReader((ln for ln in fh if not ln.startswith("#")), delimiter="\t"))


def read_drivers(path: Path) -> dict[str, tuple[str, str]]:
    """drivers.tsv -> {GEO driver name: (VFBexp class or '', note)}."""
    return {r["driver"]: (r["expression_pattern"], r["note"]) for r in _read_tsv(path)}


def read_cell_types(path: Path) -> dict[str, tuple[str, ...]]:
    """cell_types.tsv -> {author cell type: FBbt ids ('|'-separated in the file)}."""
    return {r["author_cell_type"]: tuple(c for c in r["cell_type"].split("|") if c)
            for r in _read_tsv(path)}


@dataclass
class Sample:
    title: str            # the authors' sample name (GEO title; keys its TPM table column)
    gsm: str
    biosample: str
    driver_id: str        # the GEO characteristic named by samples.driver_field
    expression_pattern: str
    author_cell_type: str = ""
    cell_types: tuple[str, ...] = ()   # FBbt ids the sample is composed primarily of
    library: str = ""     # one library of a GEO sample that pools several (samples.libraries)
    column: str = ""      # expression table column, where not derived from the title

    @property
    def name(self) -> str:
        """The sample's name: its GEO title, plus the library within a pooled GEO sample."""
        return f"{self.title}:{self.library}" if self.library else self.title


def _author_cell_type(sc: dict, title: str, driver: str) -> str | None:
    """The authors' cell type, matched from the sample title by samples.cell_type_pattern
    (a regex with a `cell_type` group; `{driver}` stands for the sample's driver)."""
    pattern = sc["cell_type_pattern"].replace("{driver}", re.escape(driver))
    m = re.search(pattern, title)
    return m.group("cell_type").strip() if m else None


def needs_table(cfg: dict) -> bool:
    """Whether select_samples needs the expression table (for samples.libraries)."""
    return bool(cfg["samples"].get("libraries"))


def _library_samples(s, sc: dict, table) -> list[tuple[str, str, str, str]]:
    """(library, column, driver, author cell type) for each library of a GEO sample that
    pools several, one expression-table column each: the columns ending in the sample's
    `column_suffix`, with driver and cell type from the table's metadata rows
    (samples.library_driver_row / library_cell_type_row)."""
    if table is None:
        raise ValueError(f"{s.accession} pools libraries (samples.libraries): pass the expression table")
    suffix = sc["libraries"][s.accession]["column_suffix"]
    drv, ct = table.meta[sc["library_driver_row"]], table.meta[sc["library_cell_type_row"]]
    out = [(c[:-len(suffix)], c, str(drv[j]).strip(), str(ct[j]).strip())
           for j, c in enumerate(table.columns) if c.endswith(suffix)]
    if not out:
        raise ValueError(f"no expression table columns end in {suffix!r} ({s.accession})")
    return out


def select_samples(series: GeoSeries, cfg: dict, table=None) -> tuple[list[Sample], list[dict]]:
    """(samples to load, [{title, gsm, reason}] left out), in GEO order.

    The driver is the GEO characteristic samples.driver_field; samples whose
    samples.driver_type_field value is in exclude_driver_types are left out. With
    samples.cell_types, each sample's author cell type (from its title) is mapped to FBbt.
    A GEO sample in samples.libraries pools several libraries, each with its own table
    column, driver and cell type (from the table's metadata rows; needs `table`): it gives
    one Sample per library. Raises on a driver missing from drivers.tsv or an author cell
    type missing from cell_types.tsv (new ones need curating)."""
    sc = cfg["samples"]
    columns = cfg.get("expression", {}).get("sample_columns", {})
    drivers = read_drivers(cfg["_dir"] / sc["drivers"])
    cell_types = read_cell_types(cfg["_dir"] / sc["cell_types"]) if sc.get("cell_types") else None
    exclude = sc.get("exclude_driver_types", {})
    keep, left_out, missing, missing_types = [], [], set(), set()
    for s in series.samples:
        dtype = (s.characteristic(sc["driver_type_field"]) or "").strip() if sc.get("driver_type_field") else ""
        if dtype in exclude:
            left_out.append({"title": s.title, "gsm": s.accession, "reason": exclude[dtype].strip()})
            continue
        if s.accession in sc.get("libraries", {}):
            parts = _library_samples(s, sc, table)
        else:
            parts = [("", columns.get(s.accession, ""), (s.characteristic(sc["driver_field"]) or "").strip(), None)]
        for library, column, driver_id, author in parts:
            name = f"{s.title}:{library}" if library else s.title
            if driver_id not in drivers:
                missing.add(driver_id)
                continue
            vfbexp, note = drivers[driver_id]
            if not vfbexp:
                left_out.append({"title": name, "gsm": s.accession, "reason": note or "no VFBexp class"})
                continue
            fbbt = ()
            if cell_types is not None:
                if author is None:
                    author = _author_cell_type(sc, s.title, driver_id)
                if author is None or author not in cell_types:
                    missing_types.add(author or f"(no match in {s.title!r})")
                    continue
                fbbt = cell_types[author]
            keep.append(Sample(s.title, s.accession, s.relations.get("BioSample", ""), driver_id, vfbexp,
                               author or "", fbbt, library, column))
    if missing:
        raise ValueError(f"drivers not in {sc['drivers']} (curate them): {sorted(missing)}")
    if missing_types:
        raise ValueError(f"author cell types not in {sc['cell_types']} (curate them): {sorted(missing_types)}")
    return keep, left_out
