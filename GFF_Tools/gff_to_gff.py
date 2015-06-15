#!/usr/bin/env python

#   A script to build a GFF annotation with a reference GFF file

import gff_extracter
import Pseudoscaffold_Tools.pseudoscaffold_tools as pseudoscaffold_tools


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


def gff_to_gff(lock, unique, extracted_sequence, reference, annotation, pseudoscaffold, outfile):
    lock.acquire()
    sources = gff_extracter.source_finder(unique, annotation, length_checker)
    types = gff_extracter.type_finder(unique, annotation, length_checker)
    scores = gff_extracter.score_finder(unique, annotation, length_checker)
    strands = gff_extracter.strandedness(unique, annotation, length_checker)
    phases = gff_extracter.phase_finder(unique, annotation, length_checker)
    attributes = gff_extracter.attribute_finder(unique, annotation, length_checker)
    contig_pseudo = pseudoscaffold_tools.contig_finder(extracted_sequence, length_checker, pseudoscaffold)
    start, end = pseudoscaffold_tools.length_gff(extracted_sequence, length_checker, pseudoscaffold)
    gff3_builder(outfile, contig_pseudo, sources, types, start, end, scores, strands, phases, attributes, length_checker)
    lock.release()
