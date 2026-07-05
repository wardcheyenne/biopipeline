"""Example: GC content statistics across a FASTA file."""
import statistics, sys
from biopipeline import FASTAReader, Pipeline

def main(path: str) -> None:
    """
    This is a function to compute and print GC content statistics for sequences in a FASTA file that pass a minimum-length filter.
    Input(s):
    - path: filesystem path to the input FASTA file
    Output(s):
    - None: prints the count, mean, median, and standard deviation of GC content to stdout
    """
    pipeline = Pipeline().map(lambda s: s if len(s) >= 50 else None, name="min_length")
    gc_values = [s.gc_content() for s in pipeline.run(FASTAReader(path), progress=True)]
    if not gc_values:
        print("No sequences passed filters."); return
    print(f"n      = {len(gc_values)}")
    print(f"mean   = {statistics.mean(gc_values):.4f}")
    print(f"median = {statistics.median(gc_values):.4f}")
    print(f"stdev  = {statistics.stdev(gc_values):.4f}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit("Usage: python gc_analysis.py <file.fasta>")
    main(sys.argv[1])
