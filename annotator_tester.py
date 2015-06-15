#!/bin/usr/env python

import re
import argparse
import argparse
import subprocess
import os
import sys

Arguments = argparse.ArgumentParser(add_help=True)
Arguments.add_argument('-a',
    '--annotation',
    type=str,
    default=None,
    metavar='ANNOTATION',
    help="Annotation file from pseudoscaffold")

Arguments.add_argument('-r',
    '--reference',
    type=str,
    default=None,
    metavar='REFERENCE',
    help="Reference fasta file if did not keep 'pseudoscaffold_annotator_temp.fasta' from generation of pseudoscaffold annotation")

Arguments.add_argument('-p',
    '--pseudoscaffold',
    type=str,
    default=None,
    metavar='PSEUDOSCAFFOLD',
    help="Pseudoscaffold file")

Arguments.add_argument('-o'
    '--original-annotation',
    type=str,
    default=None,
    metavar='ORIGINAL ANNOTATION',
    help="Original annotation file if did not keep 'pseudoscaffold_annotator_temp.fasta' from generation of pseudoscaffold annotation")

args = Arguments.parse_args()

def sequence_extracter():
    tmp = 'temp_test.fasta'
    print("Searching for original sequences using 'extraction.sh'")
#    extraction_cmd = ['bash', './Shell_Scripts/extraction.sh', args.pseudoscaffold, args.annotation, tmp]
    extraction_cmd = ['bash', './extraction.sh', args.pseudoscaffold, args.annotation, tmp]
    extraction_shell = subprocess.Popen(extraction_cmd, shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = extraction_shell.communicate()
    seq_list = open(tmp).read()
    sequence = re.compile(ur'([ACTGN]+)')
    extracter = sequence.findall(seq_list)
    os.remove(tmp)
    print("Found sequences")
    return(extracter)


def sequence_finder():
    file = re.compile("pseudoscaffold_annotator_temp.fasta")
    directory = os.listdir('.')
    dirlist = ",".join(directory)
    if file.search(dirlist):
        seq_list = open(tmp).read()
        sequence = re.compile(ur'([ACTGN]+)')
        extracter = sequence.findall(seq_list)
        os.remove(tmp)
        print("Found sequences")
        return(extracter)
    else:
        if args.original-annotation and args.reference:
            tmp = 'temp_test.fasta'
            print("Searching for original sequences using 'extraction.sh'")
            extraction_cmd = ['bash', './extraction.sh', args.reference, args.annotation, tmp]
            extraction_shell = subprocess.Popen(extraction_cmd, shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            out, err = extraction_shell.communicate()
            seq_list = open(tmp).read()
            sequence = re.compile(ur'([ACTGN]+)')
            extracter = sequence.findall(seq_list)
            os.remove(tmp)
            print("Found sequences")
            return(extracter)
        else:
            sys.exit(1)


def tester(new_sequence, original_sequence):
    same_sequences = set(new_sequence).intersection(original_sequence)
    if len(a) == len(same_sequences):
        print "All found, pseudoscaffold was successfully annotated"
    else:
        print "Failed to find all, pseudoscaffold was not successfully annotated"
        sys.exit(1)


def main():
    new_sequence = sequence_extracter()
    original_sequence = sequence_finder()
    tester(new_sequence, original_sequence)

main()
