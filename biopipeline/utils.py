"""General-purpose utilities for biopipeline."""
from __future__ import annotations
import logging
from pathlib import Path
from typing import Union, Iterable

def get_logger(name: str = "biopipeline") -> logging.Logger:
    """
    This is a function to get (or lazily configure) a named logger with a standard stream handler and formatter.
    Input(s):
    - name: the logger's name (defaults to "biopipeline")
    Output(s):
    - logging.Logger: the configured logger instance, with a handler attached only the first time it's requested
    """
    logger = logging.getLogger(name)
    if not logger.handlers:
        h = logging.StreamHandler()
        h.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s"))
        logger.addHandler(h)
    return logger

def file_size_mb(path: Union[str, Path]) -> float:
    """
    This is a function to compute the size of a file in megabytes.
    Input(s):
    - path: filesystem path (str or Path) to the file
    Output(s):
    - float: the file's size in megabytes
    """
    return Path(path).stat().st_size / (1024 * 1024)

def safe_filename(name: str) -> str:
    """
    This is a function to sanitize a string into a safe filename by replacing disallowed characters with underscores.
    Input(s):
    - name: the raw string to sanitize
    Output(s):
    - str: the sanitized filename, keeping only alphanumerics, "-", "_", and "." unchanged
    """
    return "".join(c if c.isalnum() or c in "-_." else "_" for c in name)

def chunk(lst: list, size: int) -> Iterable:
    """
    This is a function to split a list into consecutive sub-lists ("chunks") of a fixed maximum size.
    Input(s):
    - lst: the list to split
    - size: the maximum size of each chunk
    Output(s):
    - Iterable: a generator yielding successive chunks of the list
    """
    for i in range(0, len(lst), size):
        yield lst[i : i + size]
