#!/usr/bin/env python

import argparse
import subprocess
import sys
import os
import re

Arguments = argparse.ArgumentParser(add_help=True)
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

args = Arguments.parse_args()


def Usage():
    print'''Usage: Pseudoscaffold_Annotator.py -r | --reference <reference fasta> -a | --annotation <reference annotation file> -p | --pseudoscaffold <assembled pseudoscaffold fasta>'''
    return


def opener(annotations, references, pseudoscaffolds):
    annotation = open(annotations).read()
    reference = open(references).read()
    pseudoscaffold = open(psuedoscaffolds).read()
    return(annotation, reference, pseudoscaffold)


def reference_extracter():
    outfile = 'sequence.fasta'
    extraction_cmd = ['bash', './extraction.sh', args.reference, args.annotation, outfile]
    extraction_shell = subprocess.Popen(extraction_cmd, shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = extraction_shell.communicate()
    return(out, err, outfile)


def sequence_extracter(out):
    extraction = open(out)
    reader = extraction.read()
    sequence = re.compile(ur'([ACTG]+)')
    contig = re.compile(ur'(^>[a-zA-Z0-9_]+)', re.MULTILINE)
    extracter = sequence.findall(reader)
    contig_ID = contig.findall(reader)
    extraction.close()
    return(extracter, contig_ID)


def gff3_field_finder(pseudoscaffold, extraction, annotation, reference):
    pseudo_ID = list()
    for captured in extraction:
        sequence_find = re.compile(ur'(^>[0-9a-z_\s]+)(?=\s.*%s)'%(captured), re.MULTILINE | re.DOTALL)
        ID = sequence_find.search(pseudo_reader)
        print ID.groups()


def main():
    if not sys.argv[1:]:
        Usage()
        exit(1)
    else:
        annotation, reference, pseudoscaffold = opener(args.annotation, args.reference, args.pseudoscaffold)
        out, err, outfile = reference_extracter()
        extraction, contig_ID = sequence_extracter(outfile)
        gff3_field_finder()


main()
