#!/usr/bin/env python

import argparse
import subprocess
import os
import sys
import re

Arguments = argparse.ArgumentParser(add_help=True)

Arguments.add_argument('-a',
    '--annotation',
    type=str,
    default=None,
    metavar='ANNOTATION',
    help="Annotation file for reference FASTA")

Arguments.add_argument('-o',
    '--outfile',
    type=str,
    default='test_annotations.gff',
    metavar='OUTFILE',
    help="Desired name of output annotation file. Please put full file name, including extension. Defalt is 'test_annotations.gff'")

args = Arguments.parse_args()

def opener(annotation):
    annotations = open(annotation).read()
    print("Opened all files")
    return(annotations)


def contig_finder(annotation):
    contig = re.compile(ur'(^[a-zA-Z0-9_]+)', re.MULTILINE)
    contig_original = list()
    extracted_contig = contig.findall(annotation)
    del extracted_contig[72:]
    length_checker = len(extracted_contig)
    for entry in extracted_contig:
        if not entry in contig_original:
            contig_original.append(entry)
        else:
            pass
    print("Original contigs found")
    return(extracted_contig, contig_original, length_checker)


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


def start_finder(contig_original, annotation, length_checker):
    starts = list()
    for unique in contig_original:
        start_searcher = re.compile(ur'(?<=%s)\s+[a-zA-Z0-9]+\s+[a-zA-Z0-9_]+\s+([0-9]+)'%(unique))
        starter = start_searcher.findall(annotation)
        starts = starts + starter
    if len(starts) == length_checker:
        print("All 'starts' found")
        return(starts)
    else:
        sys.exit("Failed to colleced all 'start' fields from original annotation file")


def end_finder(contig_original, annotation, length_checker):
    ends = list()
    for unique in contig_original:
        end_searcher = re.compile(ur'(?<=%s)\s+[a-zA-Z0-9]+\s+[a-zA-Z0-9_]+\s+[0-9]+\s+([0-9]+)'%(unique))
        ender = end_searcher.findall(annotation)
        ends = ends + ender
    if len(ends) == length_checker:
        print("All 'ends' found")
        return(ends)
    else:
        sys.exit("Failed to find all 'end' fields from original annotation file")


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


def gff3_builder(outfile, extracted_contig, source, types, start, end, score, strand, phase, attributes, length_checker):
    gff= open(outfile, 'w')
    for i in range(0, length_checker):
        gff.write(str(extracted_contig[i]))
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
    annotation = opener(args.annotation)
    extracted_contig, contig_original, length_checker = contig_finder(annotation)
    start = start_finder(contig_original, annotation, length_checker)
    end = end_finder(contig_original, annotation, length_checker)
    source = source_finder(contig_original, annotation, length_checker)
    types = type_finder(contig_original, annotation, length_checker)
    score = score_finder(contig_original, annotation, length_checker)
    strand = strandedness(contig_original, annotation, length_checker)
    phase = phase_finder(contig_original, annotation, length_checker)
    attributes = attribute_finder(contig_original, annotation, length_checker)
    gff3_builder(args.outfile, extracted_contig, source, types, start, end, score, strand, phase, attributes, length_checker)

main()
