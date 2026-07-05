"""Tests for the Sequence class."""
import pytest
from biopipeline.sequence import Sequence, SequenceType

def test_detect_dna():
    assert Sequence("ACGTAGC").seq_type == SequenceType.DNA

def test_detect_rna():
    assert Sequence("ACGUAGC").seq_type == SequenceType.RNA

def test_detect_mixed_tu():
    assert Sequence("ACGTUACGT").seq_type == SequenceType.UNKNOWN

def test_detect_empty():
    assert Sequence("").seq_type == SequenceType.UNKNOWN

def test_gc_content():
    assert Sequence("GCGC").gc_content() == 1.0

def test_gc_excludes_n():
    assert Sequence("GCNN").gc_content() == 1.0

def test_gc_all_n():
    assert Sequence("NNNN").gc_content() == 0.0

def test_complement_dna():
    assert Sequence("ACGT").complement().seq == "TGCA"

def test_reverse_complement():
    assert Sequence("ACGT").reverse_complement().seq == "ACGT"

def test_codon_freq():
    freq = Sequence("ATGATGATG").codon_frequency()
    assert freq["ATG"] == 3

def test_len():
    assert len(Sequence("ACGT")) == 4
