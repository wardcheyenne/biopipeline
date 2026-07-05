"""Biological sequence representation and analysis."""
from __future__ import annotations
from enum import Enum
from typing import Optional, Dict

class SequenceType(Enum):
    DNA = "DNA"
    RNA = "RNA"
    PROTEIN = "PROTEIN"
    UNKNOWN = "UNKNOWN"

IUPAC_BASES = set("ACGTURYSWKMBDHVN")
VALID_DNA   = set("ACGTN")
VALID_RNA   = set("ACGUN")

class Sequence:
    def __init__(self, seq: str, seq_id: str = "", description: str = "") -> None:
        """
        This is a function to construct a Sequence object from a raw string, normalizing it to uppercase and storing its id and description.
        Input(s):
        - seq: the raw sequence string
        - seq_id: identifier for the sequence (defaults to empty string)
        - description: free-text description of the sequence (defaults to empty string)
        Output(s):
        - None: initializes the new Sequence instance's attributes
        """
        self.seq = seq.upper().strip()
        self.id  = seq_id
        self.description = description
        self._type: Optional[SequenceType] = None

    @property
    def seq_type(self) -> SequenceType:
        """
        This is a function to lazily compute and cache the sequence's detected type.
        Input(s):
        - None
        Output(s):
        - SequenceType: the detected type of the sequence, computed once and cached
        """
        if self._type is None:
            self._type = self._detect_type()
        return self._type

    def _detect_type(self) -> SequenceType:
        """
        This is a function to determine whether the sequence is DNA, RNA, or unknown based on its character content.
        Input(s):
        - None
        Output(s):
        - SequenceType: DNA, RNA, or UNKNOWN depending on which characters are present in the sequence
        """
        if not self.seq:
            return SequenceType.UNKNOWN
        chars = set(self.seq)
        if chars - IUPAC_BASES:
            return SequenceType.UNKNOWN
        if "U" in chars and "T" not in chars:
            return SequenceType.RNA
        if chars <= VALID_DNA:
            return SequenceType.DNA
        return SequenceType.UNKNOWN

    def gc_content(self) -> float:
        """
        This is a function to compute the GC content fraction of the sequence, excluding ambiguous "N" bases from the total.
        Input(s):
        - None
        Output(s):
        - float: the fraction of G/C bases out of all non-N bases, or 0.0 if there are no countable bases
        """
        total = sum(1 for b in self.seq if b != "N")
        return 0.0 if total == 0 else sum(1 for b in self.seq if b in "GC") / total

    def codon_frequency(self) -> Dict[str, int]:
        """
        This is a function to compute a codon usage table by scanning the sequence in the +0 reading frame.
        Input(s):
        - None
        Output(s):
        - Dict[str, int]: mapping of each 3-base codon to how many times it appears
        """
        if self.seq_type not in (SequenceType.DNA, SequenceType.RNA):
            raise ValueError("Codon analysis requires a nucleotide sequence")
        freq: Dict[str, int] = {}
        for i in range(0, len(self.seq) - 2, 3):
            codon = self.seq[i : i + 3]
            if len(codon) == 3:
                freq[codon] = freq.get(codon, 0) + 1
        return freq

    def complement(self) -> Sequence:
        """
        This is a function to build the complementary strand of a DNA or RNA sequence.
        Input(s):
        - None
        Output(s):
        - Sequence: a new Sequence containing the base-by-base complement, with an "_comp" suffix added to the id
        """
        if self.seq_type == SequenceType.DNA:
            table = str.maketrans("ACGTN", "TGCAN")
        elif self.seq_type == SequenceType.RNA:
            table = str.maketrans("ACGUN", "UGCAN")
        else:
            raise ValueError("Cannot complement a non-nucleotide sequence")
        return Sequence(self.seq.translate(table), f"{self.id}_comp", self.description)

    def reverse_complement(self) -> Sequence:
        """
        This is a function to build the reverse complement of a DNA or RNA sequence.
        Input(s):
        - None
        Output(s):
        - Sequence: a new Sequence containing the reversed complement strand, with an "_revcomp" suffix added to the id
        """
        c = self.complement()
        return Sequence(c.seq[::-1], f"{self.id}_revcomp", self.description)

    def __len__(self) -> int:
        """
        This is a function to report the length of the underlying sequence string.
        Input(s):
        - None
        Output(s):
        - int: the number of bases/residues in the sequence
        """
        return len(self.seq)

    def __repr__(self) -> str:
        """
        This is a function to produce a human-readable representation of the Sequence for debugging/printing.
        Input(s):
        - None
        Output(s):
        - str: a string showing the sequence's id, detected type, and length
        """
        return f"Sequence(id={self.id!r}, type={self.seq_type.value}, len={len(self)})"
