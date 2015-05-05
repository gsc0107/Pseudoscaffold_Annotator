#!/bin/usr/env python

import argparse
try:
    from pybedtools import BedTool
except ImportError:
    print("PyBedTools not found, running via subprocess instead")
    import subprocess
import os
import sys
import re

Arguments = argparse.ArgumentParser()
Arguments.add_argument('-i',
    '-input')
Arguments.add_argument()


def reference_extracter(reference, annotation):
    fasta= open (reference)
    bedfile = open(annotation)
    extracter = BedTool(bedfile)
    extracter = extracter.sequence(fi=fasta)

def reference_shell(reference, annotation):
    fasta = reference
    bedfile = annotation
    extraction = ['./extraction.sh', fasta, bedfile]
    subprocess.call(extraction)
