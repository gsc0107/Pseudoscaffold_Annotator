#!/usr/bin/env python

import argparse
#import subprocess
#import os
import sys
import re

from multiprocessing import Process, Lock

import Pseudoscaffold_Tools.pseudoscaffold_tools as pseudoscaffold_tools

Arguments = argparse.ArgumentParser(add_help=True)
Arguments.add_argument('fix',
    nargs='?',
    default=None,
    help="Fix the pseudoscaffold so that it can be annotated")
Arguments.add_argument('-r',
    '--reference',
    type=str,
    default=None,
    metavar='REFERENCE FASTA',
    help="Input reference FASTA file")

Arguments.add_argument('-a',
    '--annotation',
    type=str,
    default=None,
    metavar='ANNOTATION',
    help="Annotation file for reference FASTA")

Arguments.add_argument('-p',
    '--pseudoscaffold',
    type=str,
    default=None,
    metavar='PSEUDOSCAFFOLD FASTA',
    help="Pseudoscaffold to be annotated")

Arguments.add_argument('-o',
    '--outfile',
    type=str,
    default='pseudoscaffold_annotations.gff',
    metavar='OUTFILE',
    help="Desired name of output annotation file. Please put full file name, including extension. Defalt is 'pseudoscaffold_annotations.gff'")

args = Arguments.parse_args()


gff = re.compile(ur'(.*\.gff$)')
bed = re.compile(ur'(.*\.bed$)')


def Usage():
    print'''Usage: Pseudoscaffold_Annotator.py -r | --reference <reference fasta> -a | --annotation <reference annotation file> -p | --pseudoscaffold <assembled pseudoscaffold fasta> -o | --outfile <name of output annotation file>

Pseudoscaffold_Annotator.py creates a GFF annotation file
for an assembled pseudoscaffold fasta file based off a
reference fasta file and GFF annotation file for the
reference fasta file. Support for the BED format
will be included in a later release.

This program requires bedtools to be installed and
found within the system path. Please do this before
running Pseudscaffold_Annotator.py

***IMPORTANT***
Pseudoscaffold_Annotator.py requires no new lines
within the sequence of the pseudoscaffold.
The following is not an allowed sequence:
        >pseudoscaffold
        ACTGTCAG
        GCTATCGA

pseudoscaffold_fixer.py removes new lines
between sequence data, creating a fasta
file that reads like:
        >pseudoscaffold
        ACTGTCAGGCTATCGA
'''
    return


def opener(annotation, reference, pseudoscaffold):
    annotations = open(annotation).read()
    references = open(reference).read()
    pseudoscaffolds = open(pseudoscaffold).read()
    print("Opened all files")
    return(annotations, references, pseudoscaffolds)


def extension_searcher(gff, bed):
    find_gff = gff.search(args.annotation)
    find_bed = bed.search(args.annotation)
    return(find_gff, find_bed)


def extension_creator(gff, bed):
    create_gff = gff.search(args.outfile)
    create_bed = bed.search(args.annotation)
    return(create_gff, create_bed)


def pseudoscaffold_annotator():
    extracted_sequence = pseudoscaffold_tools.sequence_extracter(args.annotation, args.reference)
    annotation, reference, pseudoscaffold = opener(args.annotation, args.reference, args.pseudoscaffold)
    find_gff, find_bed = extension_searcher(gff, bed)
    create_gff, create_bed = extension_creator(gff, bed)
    if find_gff and create_gff:
        print "Found GFF file, making GFF file"
        import GFF_Tools.gff_to_gff as gff_to_gff
        import GFF_Tools.gff_extracter as gff_extracter
        contig_original, length_final = gff_extracter.contig_extracter(reference, annotation)
        if __name__ == '__main__':
            lock = Lock()
            for unique in contig_original:
                out=str(unique+"_out.gff")
                print out
                Process(target=gff_to_gff.gff_to_gff, args=(lock, unique, extracted_sequence, reference, annotation, pseudoscaffold, out)).start()
    elif find_gff and create_bed:
        print "Found GFF file, making BED file"
        import GFF_Tools.gff_to_bed as gff_to_bed
        import GFF_Tools.gff_extracter as gff_extracter
        contig_original, length_checker = gff_extracter.contig_extracter(reference, annotation)
        if __name__ == '__main__':
            lock = Lock()
            for unique in contig_original:
                out = str(unique+"_out.bed")
                pass
        pass
    elif find_bed and create_gff:
        print "Found BED file, making GFF file"
        import BED_Tools.bed_to_gff as bed_to_gff
        pass
    elif find_bed and create_bed:
        print "Found BED file, making BEd file"
        import BED_Tools.bed_to_bed as bed_to_bed
        pass
    else:
        sys.exit("Could not determine neither file format of input nor desired format of output file. Please make sure extensions are typed out fully.")


def main():
    if not sys.argv[1:]:
        Usage()
        exit(1)
    elif args.fix:
        import Pseuoscaffold_Tools.pseudoscaffold_fixer as pseudoscaffold_fixer
        pseudoscaffold_fixer.main(args.pseudoscaffold, args.outfile)
    else:
        pseudoscaffold_annotator()

main()
