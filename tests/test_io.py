"""Tests for IO readers."""
import tempfile, textwrap
from pathlib import Path
import pytest
from biopipeline.io import FASTAReader, FASTQReader, ParseError

FASTA = textwrap.dedent("""
    >seq1 first
    ACGTACGT
    ACGT
    >seq2
    GGGGCCCC
""").lstrip()

FASTQ = textwrap.dedent("""
    @read1 desc
    ACGTACGT
    +
    IIIIIIII
    @read2
    GGGG
    +
    IIII
""").lstrip()

def tmp(content, suffix=".fasta"):
    f = tempfile.NamedTemporaryFile(mode="w", suffix=suffix, delete=False)
    f.write(content); f.flush()
    return Path(f.name)

def test_fasta_multiline():
    seqs = list(FASTAReader(tmp(FASTA)))
    assert len(seqs) == 2
    assert seqs[0].seq == "ACGTACGTACGT"

def test_fasta_not_found():
    with pytest.raises(FileNotFoundError):
        list(FASTAReader("/no/such/file.fasta"))

def test_fastq_reads():
    records = list(FASTQReader(tmp(FASTQ, ".fastq")))
    assert len(records) == 2
    seq, qual = records[0]
    assert seq.seq == "ACGTACGT"
    assert qual == "IIIIIIII"
