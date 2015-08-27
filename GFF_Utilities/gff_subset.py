#!/usr/bin/env python

"""Subset a GFF file"""

#   Import required modules from the standard Python library
import re
import random

#   Import other modules from this software package
import gff_extracter


def gff_subset(annotation, desired_subset, out_gff):
    """Create a GFF file that's a subset of a larger GFF file"""
    contig_original, length_final = gff_extracter.contig_extracter(annotation)
    # contig_original, length_final = contig_extracter(annotation)
    print("Selecting samples for the subset")
    contig_subset = random.sample(contig_original, desired_subset)
    print("Using samples: " + str(contig_subset))
    out = open(out_gff, 'a')
    print("Opened " + out_gff + " for writing")
    for contig in contig_subset:
        contig_finder = re.compile(ur'(%s\t.*)'%(contig))
        contig_matches = contig_finder.finditer(annotation)
        while True:
            try:
                out.write(str(contig_matches.next().group()))
            except StopIteration:
                break
    out.close()


# for contig in contig_subset:
#     contig_finder = re.compile(ur'(%s\t.*)'%(contig))
#     contig_matches = contig_finder.finditer(annotation)
#     while True:
#         try:
#             print(str(contig_matches.next().group()))
#         except StopIteration:
#             break