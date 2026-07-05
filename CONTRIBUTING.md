# Contributing to biopipeline

This guide is written for researchers and data scientists who may be new to open-source workflows.

## Setup

```bash
git clone https://github.com/wardcheyenne/biopipeline.git
cd biopipeline
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
```

## Workflow

1. Branch: `git checkout -b feature/your-feature`
2. Make changes and add tests under `tests/`
3. Run `pytest` and `ruff check` before committing
4. Open a pull request against `main`

## Adding a new file reader

Implement the iterator protocol and yield `Sequence` objects:

```python
class MyFormatReader:
    def __init__(self, path): self.path = Path(path)
    def __iter__(self) -> Iterator[Sequence]: ...
```

## Adding a pipeline step

Subclass `PipelineStep`, implement `process(record)`. Return `None` to filter.

## Questions

Open a GitHub Discussion or file an issue tagged `question`.
