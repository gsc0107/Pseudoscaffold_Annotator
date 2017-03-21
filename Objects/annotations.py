#!/usr/bin/env python3

import sys
if sys.version_info.major is not 3 and sys.version_info.minor < 5:
    sys.exit("Please use Python 3.5 or higher for this module: " + __name__)


import os
from typing import Optional, TypeVar

try:
    from typeguard import typechecked
except ImportError as error:
    sys.exit("Please install " + error.name)

PlusMinus = TypeVar('PlusMinus', '+', '-')
ValidPhase = TypeVar('ValidPhase', 0, 1, 2)

class Annotation(object):
    """An annotation with three basic parts:
    Chromosome
    Start
    End"""

    def __init__(self, chrom: str, start: int, end: int) -> None:
        self._chrom = chrom
        self._start = start
        self._end = end


class BED(Annotation):
    """A BED annotation"""

    def __init__(self, chrom: str, start: int, end: int) -> None:
        super().__init__(self, chrom, start, end)


class GFF(Annotation):
    """A GFF annotation"""

    def __init__(self, seqid: str, source: str, seq_type: str, start: int, end: int, score: float, strand: PlusMinus, phase: ValidPhase) -> None:
        super().__init__(seqid, start, end)
        self._seqid = self._chrom
        self._source = source
        self._type = seq_type
        self._score = score
        self._strand = strand
        self._phase = phase


class GTF(GFF):
    """A GTF annotation"""

    def __init__(self, seqname: str, source: str, feature: str, start: int, end: int, score: float, strand: PlusMinus, frame: ValidPhase) -> None:
        super().__init__(
            seqid=seqname,
            source=source,
            seq_type=feature,
            start=start,
            end=end,
            score=score,
            strand=strand,
            phase=frame
        )
        self._feature = self._type
        self._frame = self._phase


@typechecked
def validate_annotation(annotation: str) -> str:
    """Pass an annotation file and check that it's valid"""
    try:
        return ''
    except FileNotFoundError:
        sys.exit("Failed to find " + annotation)
