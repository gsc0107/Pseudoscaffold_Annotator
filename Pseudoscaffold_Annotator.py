#!/usr/bin/env python

import argparse
import subprocess
import sys
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
    default=None,
    metavar='PSEUDOSCAFFOLD FASTA',
    help="Pseudoscaffold to be annotated")

args = Arguments.parse_args()


def Usage():
    print'''Usage: Pseudoscaffold_Annotator.py -r | --reference <reference fasta> -a | --annotation <reference annotation file> -p | --pseudoscaffold <assembled pseudoscaffold fasta>'''
    return


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
    extracter = re.findall(sequence, reader)
    return(extracter)


def sequence_matcher(pseudoscaffold, nucleotides):
    #target = BedTool(pseudoscaffold)
    #reader = target.read()
    #sequence = re.compile(nucleotides, re.M)
    #nucl = sequence.search(reader)
    #nucl = sequence.findall(reader)
    #return nucl.groups
    for captured in nucleotides:
        print captured



def main():
    if not sys.argv[1:]:
        Usage()
        exit(1)
    else:
        out, err, outfile = reference_extracter()
        extraction = sequence_extracter(outfile)
        sequence_matcher(args.pseudoscaffold, extraction)

main()
