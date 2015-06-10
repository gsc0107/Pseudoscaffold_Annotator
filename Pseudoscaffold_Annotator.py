#!/usr/bin/env python

import argparse
import subprocess
import os
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


def sequence_extracter():
    tmp = 'pseudoscaffold_annotator_temp.fasta'
    extraction_cmd = ['bash', './extraction.sh', args.reference, args.annotation, tmp]
    extraction_shell = subprocess.Popen(extraction_cmd, shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = extraction_shell.communicate()
    seq_list = open(tmp).read()
    sequence = re.compile(ur'([ACTGN]+)')
    extracter = sequence.findall(seq_list)
    #os.remove(tmp)
    return(extracter)


def opener(annotation, reference, pseudoscaffold):
    annotations = open(annotation).read()
    references = open(reference).read()
    pseudoscaffolds = open(pseudoscaffold).read()
    print("Opened all files")
    return(annotations, references, pseudoscaffolds)


def contig_finder(reference, annotation, extracted_sequence, pseudoscaffold):
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
    contig_pseudo = list()
    for captured in extracted_sequence:
        sequence_find = re.compile(ur'(^>[0-9a-z_\s]+)(?=\s.*%s)'%(captured), re.MULTILINE | re.DOTALL)
        ID = sequence_find.search(pseudoscaffold)
        contig_pseudo.append(ID.groups())
    if len(contig_pseudo) == length_checker:
        print("Pseudoscaffold contigs found")
        return(contig_original, length_checker, contig_pseudo)
    else:
        sys.exit("Failed to find all pseudoscaffold contigs")


def source_finder(contig_original, annotation, length_checker):
    sources = list()
    for unique in contig_original:
        source_searcher = re.compile(ur'(?<=%s)\s+([a-zA-Z0-9]*)'%(unique))
        sourcer = source_searcher.findall(annotation)
        sources = sources + sourcer
    if len(sources) == length_checker:
        print("All 'source' fields found")
        return(sources)
    else:
        sys.exit("Failed to collect all 'source' fields from original annotation file")


def type_finder(contig_original, annotation, length_checker):
    types = list()
    for unique in contig_original:
        type_searcher = re.compile(ur'(?<=%s)\s+[a-zA-Z0-9]+\s+([a-zA-Z0-9_]*)'%(unique))
        typer = type_searcher.findall(annotation)
        types = types + typer
    if len(types) == length_checker:
        print("All 'type' fields found")
        return(types)
    else:
        sys.exit("Failed to collect all 'type' fields from original annotation file")


def length_calculator(pseudoscaffold, extracted_sequence, length_checker):
    start = list()
    end = list()
    for extract in extracted_sequence:
        start_value = pseudoscaffold.find(extract)+1
        start.append(start_value)
        end_value = start_value+len(extract)
        end.append(end_value)
    if len(start) == len(end) == length_checker:
        print("All lengths calculated")
        return(start, end)
    else:
        sys.exit("Failed to calculate all lengths")


def score_finder(contig_original, annotation, length_checker):
    scores = list()
    for unique in contig_original:
        score_searcher = re.compile(ur'(?<=%s)\s+[a-zA-Z0-9]+\s+[a-zA-Z0-9_]+\s+[0-9]+\s+[0-9]+\s+([a-zA-Z0-9\._\-])'%(unique))
        scorer = score_searcher.findall(annotation)
        scores = scores + scorer
    if len(scores) == length_checker:
        print("All 'score' fields found'")
        return(scores)
    else:
        sys.exit("Failed to collect all 'score' fields from original annotation file")


def strandedness(contig_original, annotation, length_checker):
    strands = list()
    for unique in contig_original:
        strand_searcher = re.compile(ur'(?<=%s)\s+[a-zA-Z0-9]+\s+[a-zA-Z0-9_]+\s+[0-9]+\s+[0-9]+\s+[a-zA-Z0-9\._\-]\s+([+\-\.])'%(unique))
        strander = strand_searcher.findall(annotation)
        strands = strands + strander
    if len(strands) == length_checker:
        print("All 'strand' information found")
        return(strands)
    else:
        sys.exit("Failed to collect all 'strand' information from original annotation file")


def phase_finder(contig_original, annotation, length_checker):
    phases = list()
    for unique in contig_original:
        phase_searcher = re.compile(ur'(?<=%s)\s+[a-zA-Z0-9]+\s+[a-zA-Z0-9_]+\s+[0-9]+\s+[0-9]+\s+[a-zA-Z0-9\._\-]\s+[+\-\.]\s+([\.012])'%(unique))
        phaser = phase_searcher.findall(annotation)
        phases = phases + phaser
    if len(phases) == length_checker:
        print("All 'phase' information found")
        return(phases)
    else:
        sys.exit("Failed to collect all 'phase' information from original annotation file")


def attribute_finder(contig_original, annotation, length_checker):
    attributes = list()
    for unique in contig_original:
        attribute_searcher = re.compile(ur'(?<=%s)\s+[a-zA-Z0-9]+\s+[a-zA-Z0-9_]+\s+[0-9]+\s+[0-9]+\s+[a-zA-Z0-9\._\-]\s+[+\-\.]\s+[\.012]\s+(.*)'%(unique))
        attributer = attribute_searcher.findall(annotation)
        attributes = attributes + attributer
    if len(attributes) == length_checker:
        print("All attributes found")
        return(attributes)
    else:
        sys.exit("Failed to collect all attributes from original annotation file")


def gff3_builder(outfile, contig_pseudo, source, types, start, end, score, strand, phase, attributes, length_checker):
    gff= open(outfile, 'w')
    for i in range(0, length_checker):
        gff.write(str(contig_pseudo[i]))
        gff.write('\t')
        gff.write(str(source[i]))
        gff.write('\t')
        gff.write(str(types[i]))
        gff.write('\t')
        gff.write(str(start[i]))
        gff.write('\t')
        gff.write(str(end[i]))
        gff.write('\t')
        gff.write(str(score[i]))
        gff.write('\t')
        gff.write(str(strand[i]))
        gff.write('\t')
        gff.write(str(phase[i]))
        gff.write('\t')
        gff.write(str(attributes[i]))
        gff.write('\n')
    gff.close()
    print("GFF file created")


def main():
    if not sys.argv[1:]:
        Usage()
        exit(1)
    else:
        extracted_sequence = sequence_extracter()
        annotation, reference, pseudoscaffold = opener(args.annotation, args.reference, args.pseudoscaffold)
        contig_original, length_checker, contig_pseudo = contig_finder(reference, annotation, extracted_sequence, pseudoscaffold)
        start, end = length_calculator(pseudoscaffold, extracted_sequence, length_checker)
        source = source_finder(contig_original, annotation, length_checker)
        types = type_finder(contig_original, annotation, length_checker)
        score = score_finder(contig_original, annotation, length_checker)
        strand = strandedness(contig_original, annotation, length_checker)
        phase = phase_finder(contig_original, annotation, length_checker)
        attributes = attribute_finder(contig_original, annotation, length_checker)
        gff3_builder(args.outfile, contig_pseudo, source, types, start, end, score, strand, phase, attributes, length_checker)

main()
