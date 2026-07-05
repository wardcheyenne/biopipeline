"""YAML configuration loader for biopipeline."""
from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path
from typing import Optional
import yaml

@dataclass
class PipelineConfig:
    input_format: str = "fasta"
    batch_size: int = 1000
    output_dir: str = "output"
    log_level: str = "INFO"
    min_length: int = 0
    max_length: Optional[int] = None
    gc_min: float = 0.0
    gc_max: float = 1.0

    @classmethod
    def from_file(cls, path: str | Path) -> "PipelineConfig":
        """
        This is a function to build a PipelineConfig from a YAML file, keeping only keys that match declared config fields.
        Input(s):
        - path: filesystem path (str or Path) to the YAML configuration file
        Output(s):
        - PipelineConfig: a new config instance populated from the YAML file's recognized fields, with defaults for the rest
        """
        with open(path) as fh:
            data = yaml.safe_load(fh) or {}
        return cls(**{k: v for k, v in data.items() if k in cls.__dataclass_fields__})
