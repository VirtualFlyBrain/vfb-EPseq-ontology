"""Entity records, id keys and expression rows for a project.

Records use the slot names of the extension schema (schema/VFB_EPseq_schema.yaml);
vfb_scrnaseq.emit turns them into OWL. Ids are VFBseq ids minted in vfb-scRNAseq's
registry (scripts/write_keys.py -> vfb-scRNAseq scripts/mint_external_ids.py ->
projects/<name>/ids.tsv); NCBI/GEO accessions are xrefs.
"""

from __future__ import annotations

import csv
import gzip
from collections import defaultdict
from collections.abc import Iterator
from pathlib import Path

from vfb_scrnaseq.gene_ids import read_map

from vfb_epseq.project import Sample

VFB = "http://virtualflybrain.org/reports/"
LICENCES = {"CC-BY-4.0": "vfb:VFBlicense_CC_BY_4_0"}
KEY_COLUMNS = ["entity_type", "natural_key", "label", "accession"]


def _cite(cfg: dict) -> tuple[str, str]:
    src = cfg["source"]
    return f"{src['first_author']} ({src['year']})", f" ({src['first_author']} {src['year']})"


def dataset_label(cfg: dict) -> str:
    return f"{cfg['dataset']['label_prefix']} {_cite(cfg)[0]}"


def sample_label(cfg: dict, s: Sample) -> str:
    return f"{s.title}{_cite(cfg)[1]}"


def keys(cfg: dict, samples: list[Sample]) -> list[dict]:
    """Natural keys to mint ids for, in vfb-scRNAseq's form (`<series>`, `<series>:<sample>`)."""
    gse = cfg["source"]["geo_series"]
    rows = [{"entity_type": "Dataset", "natural_key": gse, "label": dataset_label(cfg), "accession": gse}]
    rows += [{"entity_type": "Sample", "natural_key": f"{gse}:{s.title}", "label": s.title,
              "accession": s.biosample} for s in samples]
    return rows


def write_keys(path: Path, rows: list[dict]) -> None:
    with path.open("w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=KEY_COLUMNS, delimiter="\t", lineterminator="\n")
        w.writeheader()
        w.writerows(rows)


def read_ids(path: Path) -> dict[tuple[str, str], str]:
    """ids.tsv (written by vfb-scRNAseq's mint_external_ids.py) -> {(type, natural key): id}."""
    with path.open() as fh:
        return {(r["entity_type"], r["natural_key"]): r["id"] for r in csv.DictReader(fh, delimiter="\t")}


class IdLookup:
    def __init__(self, cfg: dict, ids: dict[tuple[str, str], str]):
        self.gse, self.ids = cfg["source"]["geo_series"], ids

    def _get(self, etype: str, key: str) -> str:
        try:
            return self.ids[(etype, key)]
        except KeyError:
            raise KeyError(f"no id for {etype} {key!r}: run scripts/write_keys.py and mint the ids") from None

    def dataset(self) -> str:
        return self._get("Dataset", self.gse)

    def sample(self, s: Sample) -> str:
        return self._get("Sample", f"{self.gse}:{s.title}")


def entities(cfg: dict, samples: list[Sample], ids: IdLookup) -> list[dict]:
    src, ds, sc = cfg["source"], cfg["dataset"], cfg["samples"]
    ds_iri = VFB + ids.dataset()
    out = [{
        "type": "EPseqDataset", "id": ds_iri, "name": dataset_label(cfg), "title": ds["title"],
        "neo_label": ["DataSet"], "site": "vfb:GEO", "accession": src["geo_series"],
        "licence": LICENCES[ds["licence"]], "publication": src["publication"],
        **({"expression_atlas_xref": src["expression_atlas"]} if src.get("expression_atlas") else {}),
    }]
    for s in samples:
        out.append({
            "type": "DriverSample", "id": VFB + ids.sample(s), "name": sample_label(cfg, s),
            "associated_dataset": ds_iri, "neo_label": ["Sample"],
            "sample_tissue": [sc["tissue"]], "stage": sc["stage"],
            "expression_pattern": f"vfb:{s.expression_pattern}",
            "geo_xref": [s.gsm], **({"biosample_xref": [s.biosample]} if s.biosample else {}),
        })
    return out


def gene_map(path: Path) -> dict[str, tuple[str, str]]:
    """gene_id_map.tsv -> {input FBgn: (current FBgn, current symbol)} for kept genes."""
    _, rows = read_map(path)
    return {r["input_fbgn"]: (r["current_fbgn"], r["current_symbol"]) for r in rows if r["current_fbgn"]}


def tpm_features(path: Path) -> list[tuple[str, str]]:
    """(FBgn, symbol) rows of the TPM table, skipping non-gene rows (ERCC spike-ins)."""
    with gzip.open(path, "rt") as fh:
        rows = csv.reader(fh, delimiter="\t")
        next(rows)
        return [(r[0], r[1]) for r in rows if r[0].startswith("FBgn")]


def expression(cfg: dict, tpm: Path, samples: list[Sample], ids: IdLookup,
               genes: dict[str, tuple[str, str]]) -> Iterator[list[tuple]]:
    """Per-file chunks of expression rows (sample id, label, FBgn, symbol, TPM, None).

    TPM 0 is left out; unmapped ids (split / withdrawn) are dropped. Where several input
    ids map to one current gene (merged genes), rows identical in every sample (overlapping
    models given the same reads) count once; a gene whose input rows differ is dropped,
    since the overlap between the old models is unknown and their TPM can't be combined."""
    with gzip.open(tpm, "rt") as fh:
        rows = csv.reader(fh, delimiter="\t")
        header = next(rows)
        col = {t: i for i, t in enumerate(header)}
        missing = [s.title for s in samples if s.title not in col]
        if missing:
            raise ValueError(f"samples not in {tpm.name}: {missing}")
        distinct: dict[str, dict[tuple, list[str]]] = defaultdict(dict)
        for r in rows:
            if r[0] in genes:
                distinct[genes[r[0]][0]].setdefault(tuple(r[2:]), r)
    kept = {cur: next(iter(rs.values())) for cur, rs in distinct.items() if len(rs) == 1}
    symbols = {cur: sym for cur, sym in genes.values()}
    n = cfg["expression"]["samples_per_file"]
    for i in range(0, len(samples), n):
        chunk = []
        for s in samples[i:i + n]:
            sid, c = ids.sample(s), col[s.title]
            for cur in sorted(kept):
                v = kept[cur][c]
                if v and float(v) > 0:
                    chunk.append((sid, s.title, cur, symbols[cur], v, None))
        yield chunk
