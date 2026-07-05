"""Command-line interface for biopipeline."""
from __future__ import annotations
import argparse, sys
from pathlib import Path
from .io import FASTAReader, FASTQReader
from .utils import get_logger

logger = get_logger()

def cmd_stats(args: argparse.Namespace) -> None:
    """
    This is a function to compute and print summary statistics (count, mean length, mean GC content) for a sequence file.
    Input(s):
    - args: parsed command-line arguments containing "file" (path to the sequence file) and "format" ("fasta" or "fastq")
    Output(s):
    - None: prints statistics to stdout or an error message to stderr/log
    """
    path = Path(args.file)
    if not path.exists():
        logger.error("File not found: %s", path); sys.exit(1)
    reader = FASTAReader(path) if args.format == "fasta" else FASTQReader(path)
    count = gc_sum = length_sum = 0
    for item in reader:
        seq = item[0] if isinstance(item, tuple) else item
        count += 1; length_sum += len(seq); gc_sum += seq.gc_content()
    if count == 0:
        print("No sequences found.", file=sys.stderr); return
    print(f"Sequences  : {count}")
    print(f"Mean length: {length_sum/count:.1f}")
    print(f"Mean GC    : {gc_sum/count:.3f}")

def build_parser() -> argparse.ArgumentParser:
    """
    This is a function to build the argparse command-line parser for the biopipeline CLI, including its "stats" subcommand.
    Input(s):
    - None
    Output(s):
    - argparse.ArgumentParser: the configured parser with subcommands registered
    """
    p = argparse.ArgumentParser(prog="biopipeline", description="Bioinformatics data processing toolkit")
    sub = p.add_subparsers(dest="command", required=True)
    sp = sub.add_parser("stats", help="Summary statistics for a sequence file")
    sp.add_argument("file")
    sp.add_argument("--format", choices=["fasta","fastq"], default="fasta")
    sp.set_defaults(func=cmd_stats)
    return p

def main(argv=None) -> int:
    """
    This is a function to run the biopipeline CLI end-to-end: parse arguments and dispatch to the selected subcommand.
    Input(s):
    - argv: optional list of command-line argument strings; defaults to sys.argv when None
    Output(s):
    - int: process exit code (0 on success)
    """
    args = build_parser().parse_args(argv)
    args.func(args)
    return 0

if __name__ == "__main__":
    sys.exit(main())
