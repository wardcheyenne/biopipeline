"""Composable pipeline abstraction for sequence analysis workflows."""
from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Any, Callable, Iterable, List, Optional

try:
    from tqdm import tqdm as _tqdm
    HAS_TQDM = True
except ImportError:
    HAS_TQDM = False

class PipelineStep(ABC):
    name: str = ""
    @abstractmethod
    def process(self, record: Any) -> Optional[Any]:
        """
        This is a function to process a single record and produce the next stage's value, or None to drop the record.
        Input(s):
        - record: the record to process; type is step-specific
        Output(s):
        - Optional[Any]: the transformed record, or None if the record should be filtered out
        """
        ...
    def __repr__(self) -> str:
        """
        This is a function to produce a human-readable representation of the pipeline step.
        Input(s):
        - None
        Output(s):
        - str: the step's name (or class name if unset) followed by "()"
        """
        return f"{self.name or self.__class__.__name__}()"

class FunctionStep(PipelineStep):
    def __init__(self, fn: Callable, name: str = "") -> None:
        """
        This is a function to construct a pipeline step that wraps a plain callable.
        Input(s):
        - fn: the callable to apply to each record
        - name: optional display name for the step (defaults to the callable's __name__)
        Output(s):
        - None: initializes the step's function and name attributes
        """
        self._fn = fn; self.name = name or fn.__name__
    def process(self, record: Any) -> Optional[Any]:
        """
        This is a function to apply the wrapped callable to a single record.
        Input(s):
        - record: the record to pass to the wrapped callable
        Output(s):
        - Optional[Any]: whatever the wrapped callable returns
        """
        return self._fn(record)

class Pipeline:
    def __init__(self, *steps: PipelineStep) -> None:
        """
        This is a function to construct a Pipeline from an initial sequence of steps.
        Input(s):
        - steps: zero or more PipelineStep instances to run in order
        Output(s):
        - None: initializes the pipeline's list of steps
        """
        self.steps: List[PipelineStep] = list(steps)

    def add(self, step: PipelineStep) -> "Pipeline":
        """
        This is a function to append a step to the pipeline.
        Input(s):
        - step: the PipelineStep to add
        Output(s):
        - Pipeline: the same pipeline instance, to allow method chaining
        """
        self.steps.append(step); return self

    def map(self, fn: Callable, name: str = "") -> "Pipeline":
        """
        This is a function to append a callable to the pipeline by wrapping it in a FunctionStep.
        Input(s):
        - fn: the callable to add as a pipeline step
        - name: optional display name for the step
        Output(s):
        - Pipeline: the same pipeline instance, to allow method chaining
        """
        return self.add(FunctionStep(fn, name))

    def run(self, records: Iterable[Any], progress: bool = False) -> List[Any]:
        """
        This is a function to run every step of the pipeline over a collection of records, dropping any record for which a step returns None.
        Input(s):
        - records: an iterable of records to process
        - progress: whether to display a tqdm progress bar while iterating (only if tqdm is installed)
        Output(s):
        - List[Any]: the records that survived all steps, in order
        """
        recs = list(records)
        if progress and HAS_TQDM:
            recs = _tqdm(recs, desc="Processing")
        results = []
        for record in recs:
            cur: Optional[Any] = record
            for step in self.steps:
                cur = step.process(cur)
                if cur is None: break
            if cur is not None:
                results.append(cur)
        return results

    def run_batch(self, records: Iterable[Any], batch_size: int = 1000) -> List[Any]:
        """
        This is a function to run the pipeline over records in fixed-size batches, accumulating all results.
        Input(s):
        - records: an iterable of records to process
        - batch_size: number of records to process per batch (default 1000)
        Output(s):
        - List[Any]: the combined results from running every batch through the pipeline
        """
        from .utils import chunk
        results: List[Any] = []
        for batch in chunk(list(records), batch_size):
            results.extend(self.run(batch))
        return results

    def __repr__(self) -> str:
        """
        This is a function to produce a human-readable representation of the pipeline showing its steps in order.
        Input(s):
        - None
        Output(s):
        - str: the pipeline's steps joined by " -> " inside "Pipeline([...])"
        """
        return f"Pipeline([{' -> '.join(repr(s) for s in self.steps)}])"
