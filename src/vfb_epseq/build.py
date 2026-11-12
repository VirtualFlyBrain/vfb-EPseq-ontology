"""Entity records, id keys and expression rows for a project.

Records use the slot names of the extension schema (schema/VFB_EPseq_schema.yaml);
vfb_scrnaseq.emit turns them into OWL. Ids are VFBseq ids minted in vfb-scRNAseq's
registry (scripts/write_keys.py -> vfb-scRNAseq scripts/mint_external_ids.py ->
projects/<name>/ids.tsv); NCBI/GEO accessions are xrefs.
"""

from __future__ import annotations

import csv
import gzip
import re
from collections import defaultdict
from collections.abc import Iterator
from dataclasses import dataclass, field
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
    return f"{s.name}{_cite(cfg)[1]}"


def keys(cfg: dict, samples: list[Sample]) -> list[dict]:
    """Natural keys to mint ids for, in vfb-scRNAseq's form (`<series>`, `<series>:<sample>`,
    and `<series>:<sample>:<library>` for a library of a pooled GEO sample)."""
    gse = cfg["source"]["geo_series"]
    rows = [{"entity_type": "Dataset", "natural_key": gse, "label": dataset_label(cfg), "accession": gse}]
    rows += [{"entity_type": "Sample", "natural_key": f"{gse}:{s.name}", "label": s.name,
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
        return self._get("Sample", f"{self.gse}:{s.name}")


def entities(cfg: dict, samples: list[Sample], ids: IdLookup) -> list[dict]:
    src, ds, sc = cfg["source"], cfg["dataset"], cfg["samples"]
    ds_iri = VFB + ids.dataset()
    out = [{
        "type": "EPseqDataset", "id": ds_iri, "name": dataset_label(cfg), "title": ds["title"],
        "neo_label": ["DataSet"], "site": "vfb:GEO", "accession": src["geo_series"],
        "licence": LICENCES[ds["licence"]], "publication": src["publication"],
        **({"assay_type": ds["assay_type"]} if ds.get("assay_type") else {}),
        **({"expression_atlas_xref": src["expression_atlas"]} if src.get("expression_atlas") else {}),
    }]
    for s in samples:
        out.append({
            "type": "DriverSample", "id": VFB + ids.sample(s), "name": sample_label(cfg, s),
            "associated_dataset": ds_iri, "neo_label": ["Sample"],
            "sample_tissue": sc.get("tissue_by_cell_type", {}).get(s.author_cell_type, [sc["tissue"]]),
            "stage": sc["stage"],
            "expression_pattern": f"vfb:{s.expression_pattern}",
            **({"cell_type": list(s.cell_types)} if s.cell_types else {}),
            "geo_xref": [s.gsm], **({"biosample_xref": [s.biosample]} if s.biosample else {}),
        })
    return out


def gene_map(path: Path) -> dict[str, tuple[str, str]]:
    """gene_id_map.tsv -> {input FBgn: (current FBgn, current symbol)} for kept genes."""
    _, rows = read_map(path)
    return {r["input_fbgn"]: (r["current_fbgn"], r["current_symbol"]) for r in rows if r["current_fbgn"]}


@dataclass
class TpmTable:
    """An expression table: one column key per sample and one row per input gene id
    (FBgn, symbol, values as in the source: strings from a text table, floats from a
    spreadsheet). `meta`: a spreadsheet's per-column metadata rows (down to the header row),
    keyed by their label in the first column, aligned with `columns` and filled forward
    (a value applies to the columns after it until the next one, as in merged cells)."""
    columns: list[str]
    rows: list[tuple[str, str, list]]
    meta: dict[str, list] = field(default_factory=dict)


def _read_text(path: Path) -> TpmTable:
    """Tab-separated (gzipped) genes x samples: gene id, symbol, then one column per
    sample. Non-gene rows (e.g. ERCC spike-ins) are skipped."""
    with gzip.open(path, "rt") as fh:
        rows = csv.reader(fh, delimiter="\t")
        header = next(rows)
        return TpmTable(header[2:], [(r[0], r[1], r[2:]) for r in rows if r[0].startswith("FBgn")])


def _read_xlsx(path: Path, x: dict) -> TpmTable:
    """A spreadsheet of genes or transcripts x samples (e.g. RSEM transcript TPM, gene
    counts). Sample keys are read from row `column_row` (1-based) of the sample columns;
    gene id / symbol from the header row's `gene_column` / `symbol_column` (optional; the
    gene id where absent). Rows of one gene are summed (a gene's TPM is the sum of its
    transcripts'); rows with no FBgn (spike-ins, non-FlyBase sequences, transgenes) are
    skipped."""
    import openpyxl
    wb = openpyxl.load_workbook(path, read_only=True, data_only=True)
    try:
        rows = list(wb[x["sheet"]].iter_rows(values_only=True))
    finally:
        wb.close()
    keys, header = rows[x["column_row"] - 1], rows[x["header_row"] - 1]
    gi = header.index(x["gene_column"])
    si = header.index(x["symbol_column"]) if x.get("symbol_column") else gi
    cols = [i for i in range(len(header)) if i > max(gi, si) and keys[i] not in (None, "")
            and str(header[i] or "").startswith(x.get("sample_prefix", ""))]
    genes: dict[str, tuple[str, list[float]]] = {}
    for r in rows[x["header_row"]:]:
        g = r[gi] if gi < len(r) else None
        if not (isinstance(g, str) and g.startswith("FBgn")):
            continue
        sym, acc = genes.setdefault(g, (r[si] if si != gi and r[si] else g, [0.0] * len(cols)))
        for j, c in enumerate(cols):
            v = r[c]
            if v not in (None, ""):
                acc[j] += float(v)
    meta = {}
    for r in rows[:x["header_row"]]:
        if r and isinstance(r[0], str) and r[0].strip():
            vals, last = [], None
            for c in cols:
                v = r[c] if c < len(r) else None
                last = v if v not in (None, "") else last
                vals.append(last)
            meta[r[0].strip()] = vals
    return TpmTable([str(keys[c]) for c in cols], [(g, sym, v) for g, (sym, v) in genes.items()], meta)


def read_tpm(cfg: dict, path: Path) -> TpmTable:
    x = cfg["expression"]
    return _read_xlsx(path, x["xlsx"]) if path.suffix == ".xlsx" else _read_text(path)


def tpm_features(table: TpmTable) -> list[tuple[str, str]]:
    """(FBgn, symbol) of each gene row, for update_gene_ids.py."""
    return [(g, sym) for g, sym, _ in table.rows]


def _fmt(v) -> str:
    """Source strings as they are; summed floats rounded (clears float noise)."""
    return v if isinstance(v, str) else f"{round(v, 6):.15g}"


def sample_column(cfg: dict, s: Sample) -> str:
    """The table column of a sample: its own (`expression.sample_columns`, or a pooled
    library's), else the GEO title, or the `column` group of `expression.sample_column`
    matched against it (e.g. a sample id prefix)."""
    if s.column:
        return s.column
    pat = cfg["expression"].get("sample_column")
    if not pat:
        return s.title
    m = re.match(pat, s.title)
    if not m:
        raise ValueError(f"sample_column does not match title {s.title!r}")
    return m["column"]


def expression(cfg: dict, table: TpmTable, samples: list[Sample], ids: IdLookup,
               genes: dict[str, tuple[str, str]]) -> Iterator[list[tuple]]:
    """Per-file chunks of expression rows (sample id, label, FBgn, symbol, TPM, None).

    TPM 0 is left out; unmapped ids (split / withdrawn) are dropped. Where several input
    ids map to one current gene (merged genes), `expression.merged_genes` says how:
    `identical` (default; for tables where overlapping models may be given the same
    reads): rows identical in every sample count once, and a gene whose input rows
    differ is dropped, since the overlap between the old models is unknown; `sum`: for
    tables where each read is assigned once (e.g. RSEM's EM), the rows are summed.

    `expression.normalise: cpm` (for tables of counts) scales each sample to counts per
    million: the value over the sum of the sample's gene rows in the table (every FBgn row,
    before id mapping, so dropped ids don't rescale the rest; spike-ins and transgenes,
    which have no FBgn, are not counted)."""
    col = {t: i for i, t in enumerate(table.columns)}
    scol = {s.name: sample_column(cfg, s) for s in samples}
    missing = [t for t, c in scol.items() if c not in col]
    if missing:
        raise ValueError(f"samples not in the expression table: {missing}")
    by: dict[str, list[list]] = defaultdict(list)
    for g, _, vals in table.rows:
        if g in genes:
            by[genes[g][0]].append(vals)
    mode = cfg["expression"].get("merged_genes", "identical")
    kept: dict[str, list] = {}
    for cur, vs in by.items():
        if len(vs) == 1:
            kept[cur] = vs[0]
        elif mode == "sum":
            kept[cur] = [sum(float(v or 0) for v in t) for t in zip(*vs)]
        elif mode == "identical":
            if len({tuple(v) for v in vs}) == 1:
                kept[cur] = vs[0]
        else:
            raise ValueError(f"expression.merged_genes: {mode!r} (identical or sum)")
    norm = cfg["expression"].get("normalise")
    if norm not in (None, "cpm"):
        raise ValueError(f"expression.normalise: {norm!r} (cpm or unset)")
    scale = [1.0] * len(table.columns)
    if norm == "cpm":
        totals = [sum(float(v or 0) for v in t) for t in zip(*(vals for _, _, vals in table.rows))]
        scale = [1e6 / t if t else 0.0 for t in totals]
    symbols = {cur: sym for cur, sym in genes.values()}
    n = cfg["expression"]["samples_per_file"]
    for i in range(0, len(samples), n):
        chunk = []
        for s in samples[i:i + n]:
            sid, c = ids.sample(s), col[scol[s.name]]
            for cur in sorted(kept):
                v = kept[cur][c]
                if v and float(v) > 0:
                    v = float(v) * scale[c] if norm else v
                    chunk.append((sid, s.name, cur, symbols[cur], _fmt(v), None))
        yield chunk
