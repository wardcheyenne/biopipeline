"""Pairwise local alignment using Smith-Waterman."""
from __future__ import annotations
from dataclasses import dataclass
import numpy as np

MATCH    =  2
MISMATCH = -1
GAP      = -2

@dataclass
class AlignmentResult:
    score: float
    query_aligned: str
    target_aligned: str
    query_start: int
    target_start: int
    identity: float

def pairwise_align(query: str, target: str) -> AlignmentResult:
    """
    This is a function to compute the best local alignment between two sequences using the Smith-Waterman dynamic programming algorithm.
    Input(s):
    - query: the query sequence string
    - target: the target sequence string to align against
    Output(s):
    - AlignmentResult: the best local alignment's score, aligned query/target substrings (with gaps), their start positions, and identity fraction
    """
    q, t = query.upper(), target.upper()
    m, n = len(q), len(t)
    H = np.zeros((m + 1, n + 1), dtype=float)
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            s = MATCH if q[i-1] == t[j-1] else MISMATCH
            H[i, j] = max(0.0, H[i-1,j-1]+s, H[i-1,j]+GAP, H[i,j-1]+GAP)
    idx = np.unravel_index(int(H.argmax()), H.shape)
    i, j = int(idx[0]), int(idx[1])
    best = float(H[i, j])
    qa, ta = [], []
    qi_start = tj_start = 0
    while i > 0 and j > 0 and H[i, j] > 0:
        s = MATCH if q[i-1] == t[j-1] else MISMATCH
        if H[i,j] == H[i-1,j-1] + s:
            qa.append(q[i-1]); ta.append(t[j-1]); i -= 1; j -= 1
        elif H[i,j] == H[i-1,j] + GAP:
            qa.append(q[i-1]); ta.append("-"); i -= 1
        else:
            qa.append("-"); ta.append(t[j-1]); j -= 1
        qi_start, tj_start = i, j  # update each step so final value = true start
    qa_s = "".join(reversed(qa))
    ta_s = "".join(reversed(ta))
    ident = sum(a==b for a,b in zip(qa_s,ta_s)) / max(len(qa_s),1)
    return AlignmentResult(best, qa_s, ta_s, qi_start, tj_start, ident)
