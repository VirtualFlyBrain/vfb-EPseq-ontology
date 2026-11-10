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
        "# comment\nexternal_driver_id\texpression_pattern\tnote\n"
        "SS1\tVFBexp_FBtp1FBtp2\t\nGMR\t\tno VFBexp class\n")
    return {"_dir": tmp_path,
            "source": {"geo_series": "GSE1", "first_author": "Davis", "year": 2020,
                       "publication": "FlyBase:FBrf0244935", "expression_atlas": "E-GEOD-1"},
            "dataset": {"label_prefix": "TAPIN-seq data from", "title": "t", "licence": "CC-BY-4.0"},
            "samples": {"tissue": "FBbt:00000004", "stage": "FBdv:00005369", "drivers": "drivers.tsv",
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


SAMPLES = [Sample("a_rep1", "GSM1", "SAMN1", "SS1", "VFBexp_FBtp1FBtp2"),
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
    ents = build.entities(cfg, SAMPLES, build.IdLookup(cfg, IDS))
    text = emit_owl(ents, tmp_path / "out.ofn", schema_path=SCHEMA).read_text()
    s = "VFBseq:00000002"
    for ax in (f"ClassAssertion(FBcv:0003024 {s})", f"ClassAssertion(vfb:VFBexp_FBtp1FBtp2 {s})",
               f"ClassAssertion(ObjectSomeValuesFrom(RO:0002131 FBbt:00000004) {s})",
               f"AnnotationAssertion(dc:source {s} VFBseq:00000001)",
               f'AnnotationAssertion(rdfs:label {s} "a_rep1 (Davis 2020)")',
               'neo_custom:accession "SAMN1"', 'neo_custom:accession "E-GEOD-1"',
               "ClassAssertion(FBcv:0003023 VFBseq:00000001)"):
        assert ax in text, ax


def test_expression(cfg, tmp_path):
    tpm = tmp_path / "tpm.txt.gz"
    with gzip.open(tpm, "wt") as fh:
        fh.write("gene_id\tgene_name\ta_rep1\tb_rep1\tctl\n"
                 "FBgn1\tg1\t1.5\t0\t9\n"          # 0 left out
                 "FBgn2\told2\t2\t3\t9\n"          # merged with FBgn3 (different values: summed)
                 "FBgn3\told3\t0.25\t1\t9\n"
                 "FBgn4\tdup\t4\t5\t9\n"           # FBgn4 and FBgn5 identical: counted once
                 "FBgn5\tdup2\t4\t5\t9\n"
                 "FBgn6\tsplit\t7\t7\t9\n"         # not in the map: dropped
                 "ERCC-1\tERCC-1\t1\t1\t1\n")
    genes = {"FBgn1": ("FBgn1", "g1"), "FBgn2": ("FBgn9", "m"), "FBgn3": ("FBgn9", "m"),
             "FBgn4": ("FBgn8", "d"), "FBgn5": ("FBgn8", "d")}
    assert build.tpm_features(tpm)[-1] == ("FBgn6", "split")
    chunks = list(build.expression(cfg, tpm, SAMPLES, build.IdLookup(cfg, IDS), genes))
    assert len(chunks) == 2                                   # samples_per_file 1
    got = {(r[0], r[2]): r[4] for c in chunks for r in c}
    assert got == {("VFBseq_00000002", "FBgn1"): "1.5", ("VFBseq_00000002", "FBgn9"): "2.25",
                   ("VFBseq_00000002", "FBgn8"): "4",
                   ("VFBseq_00000003", "FBgn9"): "4", ("VFBseq_00000003", "FBgn8"): "5"}
