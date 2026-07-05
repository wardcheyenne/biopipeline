# biopipeline

A modular Python toolkit for bioinformatics data processing, designed for
researchers and data scientists working with genomic sequence data.

## Features

- **Sequence analysis** - GC content, codon frequency, complement, reverse complement
- **Format support** - FASTA, FASTQ, and GenBank flat file parsers
- **Composable pipelines** - chain steps into reproducible analysis workflows
- **Pairwise alignment** - Smith-Waterman local alignment with identity scoring
- **CLI** - `biopipeline stats` for quick file summaries
- **Batch processing** - memory-efficient handling of large files with optional progress bar

## Installation

```bash
git clone https://github.com/wardcheyenne/biopipeline.git
cd biopipeline && pip install -e ".[dev]"
```

## Quick start

```python
from biopipeline import FASTAReader, Pipeline

pipeline = (
    Pipeline()
    .map(lambda s: s if len(s) >= 100 else None, name="length_filter")
    .map(lambda s: s if s.gc_content() > 0.4 else None, name="gc_filter")
)

results = pipeline.run(FASTAReader("sequences.fasta"), progress=True)
print(f"{len(results)} sequences passed filters")
```

## CLI

```bash
biopipeline stats sequences.fasta
biopipeline stats reads.fastq --format fastq
```

## Running tests

```bash
pytest tests/ -q
```

## Onboarding

See [CONTRIBUTING.md](CONTRIBUTING.md) for setup instructions and a guide to
adding new file format readers or pipeline steps.
