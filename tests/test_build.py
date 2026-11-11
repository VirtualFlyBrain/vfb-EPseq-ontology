"""Sample selection, entity records (validated + emitted with the extension schema) and
expression rows, on a small synthetic project."""

import gzip

import pytest
from vfb_scrnaseq.ingest import GeoSample, GeoSeries

from vfb_epseq import build
from vfb_epseq.project import SCHEMA, Sample, select_samples


def _gsm(acc, title, dtype, driver):
    return GeoSample(acc, title, characteristics={"driver type": dtype, "external driver id": driver},
                     relations={"BioSample": "SAMN" + acc[3:]})


@pytest.fixture
def cfg(tmp_path):
    (tmp_path / "drivers.tsv").write_text(
        "# comment\ndriver\texpression_pattern\tnote\n"
        "SS1\tVFBexp_FBtp1FBtp2\t\nGMR\t\tno VFBexp class\n")
    return {"_dir": tmp_path,
            "source": {"geo_series": "GSE1", "first_author": "Davis", "year": 2020,
                       "publication": "FlyBase:FBrf0244935", "expression_atlas": "E-GEOD-1"},
            "dataset": {"label_prefix": "TAPIN-seq data from", "title": "t", "licence": "CC-BY-4.0"},
            "samples": {"tissue": "FBbt:00000004", "stage": "FBdv:00005369", "drivers": "drivers.tsv",
                        "driver_field": "external driver id", "driver_type_field": "driver type",
                        "exclude_driver_types": {"control": "controls"}},
            "expression": {"samples_per_file": 1}}


def test_select_samples(cfg):
    series = GeoSeries("GSE1", samples=[
        _gsm("GSM1", "a_rep1", "single", "SS1"), _gsm("GSM2", "ctl", "control", "NA"),
        _gsm("GSM3", "r_rep1", "single", "GMR")])
    keep, out = select_samples(series, cfg)
    assert [s.title for s in keep] == ["a_rep1"] and keep[0].expression_pattern == "VFBexp_FBtp1FBtp2"
    assert {o["gsm"]: o["reason"] for o in out} == {"GSM2": "controls", "GSM3": "no VFBexp class"}
    series.samples.append(_gsm("GSM4", "new", "single", "SS9"))
    with pytest.raises(ValueError, match="SS9"):
        select_samples(series, cfg)


def test_select_samples_cell_types(cfg):
    (cfg["_dir"] / "cell_types.tsv").write_text(
        "author_cell_type\tcell_type\tlabel\tnote\n"
        "PAM-g5\tFBbt:00111015\t\t\nPAM-b1, PAM-b2\tFBbt:00110994|FBbt:00110993\t\t\n")
    cfg["samples"].update(cell_types="cell_types.tsv", cell_type_pattern=r"_(?P<cell_type>[^_]+)_{driver}_")
    series = GeoSeries("GSE1", samples=[
        _gsm("GSM1", "15_10_8_PAM-g5_SS1_nlsGFP_F", "single", "SS1"),
        _gsm("GSM2", "14_10_4_PAM-b1, PAM-b2_SS1_x", "single", "SS1")])
    keep, _ = select_samples(series, cfg)
    assert [(s.author_cell_type, s.cell_types) for s in keep] == [
        ("PAM-g5", ("FBbt:00111015",)), ("PAM-b1, PAM-b2", ("FBbt:00110994", "FBbt:00110993"))]
    series.samples.append(_gsm("GSM3", "1_2_KC-x_SS1_y", "single", "SS1"))
    with pytest.raises(ValueError, match="KC-x"):
        select_samples(series, cfg)


SAMPLES = [Sample("a_rep1", "GSM1", "SAMN1", "SS1", "VFBexp_FBtp1FBtp2", "PAM-g5", ("FBbt:00111015",)),
           Sample("b_rep1", "GSM2", "SAMN2", "SS1", "VFBexp_FBtp1FBtp2")]
IDS = {("Dataset", "GSE1"): "VFBseq_00000001", ("Sample", "GSE1:a_rep1"): "VFBseq_00000002",
       ("Sample", "GSE1:b_rep1"): "VFBseq_00000003"}


def test_keys_and_labels(cfg):
    rows = build.keys(cfg, SAMPLES)
    assert rows[0] == {"entity_type": "Dataset", "natural_key": "GSE1",
                       "label": "TAPIN-seq data from Davis (2020)", "accession": "GSE1"}
    assert rows[1]["natural_key"] == "GSE1:a_rep1" and rows[1]["accession"] == "SAMN1"


def test_missing_id(cfg):
    with pytest.raises(KeyError, match="write_keys"):
        build.IdLookup(cfg, {}).dataset()


def test_entities_emit(cfg, tmp_path):
    from vfb_scrnaseq.emit import emit_owl
    cfg["dataset"]["assay_type"] = "FBcv:0009018"
    ents = build.entities(cfg, SAMPLES, build.IdLookup(cfg, IDS))
    text = emit_owl(ents, tmp_path / "out.ofn", schema_path=SCHEMA).read_text()
    s = "VFBseq:00000002"
    for ax in (f"ClassAssertion(FBcv:0003024 {s})", f"ClassAssertion(vfb:VFBexp_FBtp1FBtp2 {s})",
               f"ClassAssertion(ObjectSomeValuesFrom(RO:0002131 FBbt:00000004) {s})",
               f"ClassAssertion(ObjectSomeValuesFrom(RO:0002473 FBbt:00111015) {s})",
               f"AnnotationAssertion(dc:source {s} VFBseq:00000001)",
               f'AnnotationAssertion(rdfs:label {s} "a_rep1 (Davis 2020)")',
               'neo_custom:accession "SAMN1"', 'neo_custom:accession "E-GEOD-1"',
               "ClassAssertion(FBcv:0003023 VFBseq:00000001)",
               "ClassAssertion(ObjectSomeValuesFrom(OBI:0000312 FBcv:0009018) VFBseq:00000001)"):
        assert ax in text, ax
    assert text.count("RO:0002473") == 1                       # b_rep1 has no cell type


def test_expression(cfg, tmp_path):
    tpm = tmp_path / "tpm.txt.gz"
    with gzip.open(tpm, "wt") as fh:
        fh.write("gene_id\tgene_name\ta_rep1\tb_rep1\tctl\n"
                 "FBgn1\tg1\t1.5\t0\t9\n"          # 0 left out
                 "FBgn2\told2\t2\t3\t9\n"          # merged with FBgn3, different values: dropped
                 "FBgn3\told3\t0.25\t1\t9\n"
                 "FBgn4\tdup\t4\t5\t9\n"           # FBgn4 and FBgn5 identical: counted once
                 "FBgn5\tdup2\t4\t5\t9\n"
                 "FBgn6\tsplit\t7\t7\t9\n"         # not in the map: dropped
                 "ERCC-1\tERCC-1\t1\t1\t1\n")
    genes = {"FBgn1": ("FBgn1", "g1"), "FBgn2": ("FBgn9", "m"), "FBgn3": ("FBgn9", "m"),
             "FBgn4": ("FBgn8", "d"), "FBgn5": ("FBgn8", "d")}
    table = build.read_tpm(cfg, tpm)
    assert build.tpm_features(table)[-1] == ("FBgn6", "split")
    chunks = list(build.expression(cfg, table, SAMPLES, build.IdLookup(cfg, IDS), genes))
    assert len(chunks) == 2                                   # samples_per_file 1
    got = {(r[0], r[2]): r[4] for c in chunks for r in c}
    assert got == {("VFBseq_00000002", "FBgn1"): "1.5", ("VFBseq_00000002", "FBgn8"): "4",
                   ("VFBseq_00000003", "FBgn8"): "5"}
    cfg["expression"]["merged_genes"] = "sum"
    got = {(r[0], r[2]): r[4] for c in build.expression(cfg, table, SAMPLES, build.IdLookup(cfg, IDS), genes)
           for r in c}
    assert got[("VFBseq_00000002", "FBgn9")] == "2.25" and got[("VFBseq_00000002", "FBgn8")] == "8"


def test_xlsx(cfg, tmp_path):
    openpyxl = pytest.importorskip("openpyxl")
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "m"
    ws.append([None, None, None, "Driver", "SS1", "SS1", "SS2"])
    ws.append([None, None, None, "PID", "1_1", "1_2", "9_9"])
    ws.append(["transcript", "gene_ID", "gene_symbol", None, "Sample_PID_1_1", "Sample_1_2", "Sample_9_9"])
    ws.append(["FBtr1", "FBgn1", "g1", None, 0.1, 1, 5])
    ws.append(["FBtr2", "FBgn1", "g1", None, 0.2, 0, 5])    # transcripts summed per gene
    ws.append(["DQ1", None, None, None, 7, 7, 7])           # no FBgn: skipped
    ws.append(["FBtr3", "FBgn2", "g2", None, 0, 2.5, 5])
    path = tmp_path / "t.xlsx"
    wb.save(path)
    cfg["expression"].update(xlsx={"sheet": "m", "column_row": 2, "header_row": 3, "gene_column": "gene_ID",
                                   "symbol_column": "gene_symbol", "sample_prefix": "Sample_"},
                             sample_column=r"(?P<column>\d+_\d+)_")
    table = build.read_tpm(cfg, path)
    assert table.columns == ["1_1", "1_2", "9_9"] and build.tpm_features(table) == [("FBgn1", "g1"), ("FBgn2", "g2")]
    samples = [Sample("1_1_KC_SS1", "GSM1", "", "SS1", "VFBexp_FBtp1FBtp2"),
               Sample("1_2_KC_SS1", "GSM2", "", "SS1", "VFBexp_FBtp1FBtp2")]
    ids = build.IdLookup(cfg, {("Sample", "GSE1:1_1_KC_SS1"): "VFBseq_00000002",
                               ("Sample", "GSE1:1_2_KC_SS1"): "VFBseq_00000003"})
    genes = {"FBgn1": ("FBgn1", "g1"), "FBgn2": ("FBgn2", "g2")}
    got = {(r[0], r[2]): r[4] for c in build.expression(cfg, table, samples, ids, genes) for r in c}
    assert got == {("VFBseq_00000002", "FBgn1"): "0.3", ("VFBseq_00000003", "FBgn1"): "1",
                   ("VFBseq_00000003", "FBgn2"): "2.5"}
    with pytest.raises(ValueError, match="does not match"):
        build.sample_column(cfg, Sample("x", "GSM9", "", "SS1", ""))
