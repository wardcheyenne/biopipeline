"""Example: pairwise local alignment."""
from biopipeline import pairwise_align

def main() -> None:
    """
    This is a function to demonstrate pairwise local alignment by aligning two example sequences and printing the result.
    Input(s):
    - None
    Output(s):
    - None: prints the alignment score, identity, and aligned query/target strings to stdout
    """
    result = pairwise_align("ACGTACGTACGT", "TACGTACGTACGTA")
    print(f"Score    : {result.score:.1f}")
    print(f"Identity : {result.identity:.2%}")
    print(f"Query    : {result.query_aligned}")
    print(f"Target   : {result.target_aligned}")

if __name__ == "__main__":
    main()
