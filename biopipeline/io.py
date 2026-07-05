"""File readers for common bioinformatics formats."""
from __future__ import annotations
from pathlib import Path
from typing import Iterator
from .sequence import Sequence

class ParseError(ValueError):
    pass

class FASTAReader:
    def __init__(self, path: str | Path) -> None:
        """
        This is a function to construct a FASTA file reader bound to a given path, validating that the file exists.
        Input(s):
        - path: filesystem path (str or Path) to the FASTA file
        Output(s):
        - None: initializes the reader's path attribute; raises FileNotFoundError if the file does not exist
        """
        self.path = Path(path)
        if not self.path.exists():
            raise FileNotFoundError(f"File not found: {self.path}")

    def __iter__(self) -> Iterator[Sequence]:
        """
        This is a function to iterate over the FASTA file, yielding one Sequence per record.
        Input(s):
        - None
        Output(s):
        - Iterator[Sequence]: yields a Sequence object for each ">"-delimited record in the file
        """
        seq_id = desc = ""
        buf: list[str] = []
        with self.path.open() as fh:
            for lineno, raw in enumerate(fh, 1):
                line = raw.strip()
                if line.startswith(">"):
                    if buf:
                        yield Sequence("".join(buf), seq_id, desc)
                        buf = []
                    parts = line[1:].split(None, 1)
                    seq_id = parts[0] if parts else f"seq_{lineno}"
                    desc   = parts[1] if len(parts) > 1 else ""
                elif line:
                    buf.append(line)
            if buf:
                yield Sequence("".join(buf), seq_id, desc)

class FASTQReader:
    def __init__(self, path: str | Path) -> None:
        """
        This is a function to construct a FASTQ file reader bound to a given path, validating that the file exists.
        Input(s):
        - path: filesystem path (str or Path) to the FASTQ file
        Output(s):
        - None: initializes the reader's path attribute; raises FileNotFoundError if the file does not exist
        """
        self.path = Path(path)
        if not self.path.exists():
            raise FileNotFoundError(f"File not found: {self.path}")

    def __iter__(self) -> Iterator[tuple[Sequence, str]]:
        """
        This is a function to iterate over the FASTQ file four lines at a time, yielding each record's sequence and quality string.
        Input(s):
        - None
        Output(s):
        - Iterator[tuple[Sequence, str]]: yields (Sequence, quality_string) pairs for each record; raises ParseError on a malformed header line
        """
        with self.path.open() as fh:
            lineno = 0
            while True:
                header = fh.readline()
                if not header: break
                lineno += 1
                header = header.rstrip("\n")
                if not header.startswith("@"):
                    raise ParseError(f"Expected @ at line {lineno}")
                seq_line = fh.readline().rstrip("\n"); lineno += 1
                fh.readline(); lineno += 1
                qual = fh.readline().rstrip("\n"); lineno += 1
                parts = header[1:].split(None, 1)
                yield Sequence(seq_line, parts[0] if parts else f"r{lineno}",
                               parts[1] if len(parts) > 1 else ""), qual

class GenBankReader:
    """Parse sequences from a GenBank flat file (.gb / .gbk)."""
    def __init__(self, path: str | Path) -> None:
        """
        This is a function to construct a GenBank file reader bound to a given path, validating that the file exists.
        Input(s):
        - path: filesystem path (str or Path) to the GenBank (.gb/.gbk) file
        Output(s):
        - None: initializes the reader's path attribute; raises FileNotFoundError if the file does not exist
        """
        self.path = Path(path)
        if not self.path.exists():
            raise FileNotFoundError(f"File not found: {self.path}")

    def __iter__(self) -> Iterator[Sequence]:
        """
        This is a function to iterate over a GenBank flat file, yielding one Sequence per LOCUS record found in the ORIGIN section.
        Input(s):
        - None
        Output(s):
        - Iterator[Sequence]: yields a Sequence for each record, built from its LOCUS id, DEFINITION description, and ORIGIN bases
        """
        seq_id = desc = ""; in_origin = False; bases: list[str] = []
        with self.path.open() as fh:
            for line in fh:
                if line.startswith("LOCUS"):
                    seq_id = line.split()[1]
                elif line.startswith("DEFINITION"):
                    desc = line[12:].strip()
                elif line.startswith("ORIGIN"):
                    in_origin = True; bases = []
                elif line.startswith("//"):
                    if bases:
                        yield Sequence("".join(bases).upper(), seq_id, desc)
                    in_origin = False
                elif in_origin:
                    bases.extend(c for c in line if c.isalpha())
