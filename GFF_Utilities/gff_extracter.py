#!/usr/bin/env python

"""A script to hold functions for finding fields in a GFF file"""

#   Import required modules from standard Python library
import re
import sys

#       Find the seqid (column 1) from the GFF file
def contig_extracter(annotation):
    """Extract the contig IDs from the original annotation file. Also provides one last check to make sure all information was transfered from original annotation file to annotation file for pseudoscaffold"""
    contig = re.compile(ur'(^[a-zA-Z0-9_]+)', re.MULTILINE)
    contig_original = list()
    extracted_contig = contig.findall(annotation)
    length_checker = len(extracted_contig)
    for entry in extracted_contig:
        if not entry in contig_original:
            contig_original.append(entry)
        else:
            pass
    print("Original contigs found")
    return(contig_original, length_checker)


#   A class to handle extracting information from the original annotation file
class gff_extracter(object):
    def __init__(self, unique, annotation, length_checker):
        self.unique = unique
        self.annotation = annotation
        self.length_checker = length_checker

    #       Find the source (column 2) from the GFF file
    def source_finder(self):
        """Find the source information from the original annotation file."""
        source_searcher = re.compile(ur'(?<=%s)\s+([a-zA-Z0-9]*)'%(self.unique))
        sources = source_searcher.findall(self.annotation)
        if len(sources) == self.length_checker:
            print("All 'source' fields found")
            return(sources)
        else:
            sys.exit("Failed to collect all 'source' fields from original annotation file")

    #       Find the type (column 3) from the GFF file
    def type_finder(self):
        """Find the type information from the original annotation file."""
        type_searcher = re.compile(ur'(?<=%s)\s+[a-zA-Z0-9]+\s+([a-zA-Z0-9_]*)'%(self.unique))
        types = type_searcher.findall(self.annotation)
        if len(types) == self.length_checker:
            print("All 'type' fields found")
            return(types)
        else:
            sys.exit("Failed to collect all 'type' fields from original annotation file")

    #       Find the score (column 6) from the GFF file
    def score_finder(self):
        """Find the score information from the original annotation file."""
        score_searcher = re.compile(ur'(?<=%s)\s+[a-zA-Z0-9]+\s+[a-zA-Z0-9_]+\s+[0-9]+\s+[0-9]+\s+([a-zA-Z0-9\._\-])'%(unique))
        scores = score_searcher.findall(annotation)
        if len(scores) == length_checker:
            print("All 'score' fields found'")
            return(scores)
        else:
            sys.exit("Failed to collect all 'score' fields from original annotation file")

    #       Find the strand information (column 7) from the GFF file
    def strandedness(self):
        """Find the strand information from the original annotation file."""
        strand_searcher = re.compile(ur'(?<=%s)\s+[a-zA-Z0-9]+\s+[a-zA-Z0-9_]+\s+[0-9]+\s+[0-9]+\s+[a-zA-Z0-9\._\-]\s+([+\-\.])'%(self.unique))
        strands = strand_searcher.findall(self.annotation)
        if len(strands) == self.length_checker:
            print("All 'strand' information found")
            return(strands)
        else:
            sys.exit("Failed to collect all 'strand' information from original annotation file")

    #       Find the phase (column 8) from the GFF file
    def phase_finder(self):
        """Find the phase information from the original annotation file."""
        phase_searcher = re.compile(ur'(?<=%s)\s+[a-zA-Z0-9]+\s+[a-zA-Z0-9_]+\s+[0-9]+\s+[0-9]+\s+[a-zA-Z0-9\._\-]\s+[+\-\.]\s+([\.012])'%(self.unique))
        phases = phase_searcher.findall(self.annotation)
        if len(phases) == self.length_checker:
            print("All 'phase' information found")
            return(phases)
        else:
            sys.exit("Failed to collect all 'phase' information from original annotation file")

    #       Find any attributes (column 9) from the GFF file
    def attribute_finder(self):
        """Find the attribute information from the original annotation file."""
        attribute_searcher = re.compile(ur'(?<=%s)\s+[a-zA-Z0-9]+\s+[a-zA-Z0-9_]+\s+[0-9]+\s+[0-9]+\s+[a-zA-Z0-9\._\-]\s+[+\-\.]\s+[\.012]\s+(.*)'%(self.unique))
        attributes = attribute_searcher.findall(self.annotation)
        if len(attributes) == self.length_checker:
            print("All attributes found")
            return(attributes)
        else:
            sys.exit("Failed to collect all attributes from original annotation file")
