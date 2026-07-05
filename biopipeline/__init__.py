"""BioPipeline: A modular Python toolkit for bioinformatics data processing."""
from .sequence import Sequence, SequenceType
from .io import FASTAReader, FASTQReader, GenBankReader, ParseError
from .pipeline import Pipeline, PipelineStep, FunctionStep
from .alignment import pairwise_align, AlignmentResult
from .config import PipelineConfig

__version__ = "0.1.0"
__all__ = ["Sequence","SequenceType","FASTAReader","FASTQReader","GenBankReader",
           "ParseError","Pipeline","PipelineStep","FunctionStep",
           "pairwise_align","AlignmentResult","PipelineConfig"]
