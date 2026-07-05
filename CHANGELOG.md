# Changelog

## [Unreleased]

## [0.1.0] - 2026-07-04

### Added
- `Sequence` class: GC content, codon frequency, complement, reverse complement
- `FASTAReader`, `FASTQReader`, `GenBankReader` - generator-based format parsers
- `Pipeline` / `PipelineStep` / `FunctionStep` - composable analysis workflows
- `pairwise_align` - Smith-Waterman local sequence alignment with identity scoring
- `PipelineConfig` - YAML-driven configuration
- CLI: `biopipeline stats`
- Batch processing with optional tqdm progress bar
- GitHub Actions CI (Python 3.10–3.12)
- Example scripts: `gc_analysis.py`, `alignment_demo.py`

### Fixed
- Sequence type detection for ambiguous IUPAC bases (T+U co-presence)
- GC content edge cases: empty sequences and all-N sequences
- Smith-Waterman traceback off-by-one in start position
- FASTA parser memory usage - fully generator-based
- FASTA multi-line sequence support
