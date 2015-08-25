#!/usr/bin/env python

"""A script to subset an annotation file"""

#   Import required modules from the standard Python library
import sys
import os

#   Import modules bundled with this software package
import annotation_utilities

def subset_annotation(args, gff, bed):
    """Create a subset of an annotation file"""
    #   Read the annotation file
    annotation = open(args['annotation']).read
    find_gff, find_bed = annotation_utilities.extension_searcher(gff, bed, args['annotation'])
    basename = os.path.basename(args['annotation'])
    base = basename.split('.')[0]
    if find_gff:
        import GFF_Utilities.gff_subset as gff_subset
        out_gff = str(base + ".gff")
        gff_subset.gff_subset(annotation, args['desired'], out_gff)
    elif find_bed:
        print("Functionality not yet implemented")
        sys.exit(1)
    else:
        print("Could not identify type of annotation file")
        sys.exit(1)
