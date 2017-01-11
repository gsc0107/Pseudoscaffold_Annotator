#!/usr/bin/env python

"""A script to hold functions for finding fields in a GFF file"""

#   Import required modules from standard Python library
import re
import sys


#       Find the source (column 2) from the GFF file
def source_finder(unique, annotation, length_checker):
    """Find the source information from the original annotation file."""
    source_searcher = re.compile(r'(?<=%s)\s+([a-zA-Z0-9]*)'%(unique))
    sources = source_searcher.findall(annotation)
    if len(sources) == length_checker:
        print("All 'source' fields found")
        return(sources)
    else:
        sys.exit("Failed to collect all 'source' fields from original annotation file")


#       Find the type (column 3) from the GFF file
def type_finder(unique, annotation, length_checker):
    """Find the type information from the original annotation file."""
    type_searcher = re.compile(r'(?<=%s)\s+[a-zA-Z0-9]+\s+([a-zA-Z0-9_]*)'%(unique))
    types = type_searcher.findall(annotation)
    if len(types) == length_checker:
        print("All 'type' fields found")
        return(types)
    else:
        sys.exit("Failed to collect all 'type' fields from original annotation file")


#Find the score (column 6) from the GFF file
def score_finder(unique, annotation, length_checker):
    """Find the score information from the original annotation file."""
    score_searcher = re.compile(r'(?<=%s)\s+[a-zA-Z0-9]+\s+[a-zA-Z0-9_]+\s+[0-9]+\s+[0-9]+\s+([a-zA-Z0-9\._\-])'%(unique))
    scores = score_searcher.findall(annotation)
    if len(scores) == length_checker:
        print("All 'score' fields found'")
        return(scores)
    else:
        sys.exit("Failed to collect all 'score' fields from original annotation file")


#       Find the strand information (column 7) from the GFF file
def strandedness(unique, annotation, length_checker):
    """Find the strand information from the original annotation file."""
    strand_searcher = re.compile(r'(?<=%s)\s+[a-zA-Z0-9]+\s+[a-zA-Z0-9_]+\s+[0-9]+\s+[0-9]+\s+[a-zA-Z0-9\._\-]\s+([+\-\.])'%(unique))
    strands = strand_searcher.findall(annotation)
    if len(strands) == length_checker:
        print("All 'strand' information found")
        return(strands)
    else:
        sys.exit("Failed to collect all 'strand' information from original annotation file")


    #       Find the phase (column 8) from the GFF file
def phase_finder(unique, annotation, length_checker):
    """Find the phase information from the original annotation file."""
    phase_searcher = re.compile(r'(?<=%s)\s+[a-zA-Z0-9]+\s+[a-zA-Z0-9_]+\s+[0-9]+\s+[0-9]+\s+[a-zA-Z0-9\._\-]\s+[+\-\.]\s+([\.012])'%(unique))
    phases = phase_searcher.findall(annotation)
    if len(phases) == length_checker:
        print("All 'phase' information found")
        return(phases)
    else:
        sys.exit("Failed to collect all 'phase' information from original annotation file")


#       Find any attributes (column 9) from the GFF file
def attribute_finder(unique, annotation, length_checker):
    """Find the attribute information from the original annotation file."""
    attribute_searcher = re.compile(r'(?<=%s)\s+[a-zA-Z0-9]+\s+[a-zA-Z0-9_]+\s+[0-9]+\s+[0-9]+\s+[a-zA-Z0-9\._\-]\s+[+\-\.]\s+[\.012]\s+(.*)'%unique)
    attributes = attribute_searcher.findall(annotation)
    if len(attributes) == length_checker:
        print("All 'attributes' found")
        return(attributes)
    else:
        sys.exit("Failed to collect all attributes from original annotation file")
