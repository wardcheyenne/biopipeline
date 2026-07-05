"""Tests for Pipeline."""
from biopipeline.pipeline import Pipeline, FunctionStep
from biopipeline.sequence import Sequence

mk = lambda s: Sequence(s)

def test_filter():
    p = Pipeline().map(lambda s: s if len(s) >= 4 else None)
    assert len(p.run([mk("ACGT"), mk("AC"), mk("ACGTACGT")])) == 2

def test_filter_all():
    assert Pipeline().map(lambda _: None).run([mk("ACGT")]) == []

def test_batch():
    p = Pipeline().map(lambda s: s)
    assert len(p.run_batch([mk("ACGT")] * 50, batch_size=10)) == 50
