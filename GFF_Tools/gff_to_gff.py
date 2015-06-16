#!/usr/bin/env python

"""A script to build a GFF annotation with a reference GFF file"""

#   Import required modules from standard Python library
import re
import gff_extracter

#   Import functions defined in another script bundled with this package
import Pseudoscaffold_Tools.pseudoscaffold_tools as pseudoscaffold_tools


#   Find the number of times this a contig shows up in original annotaiton file
def find_length(unique, annotation):
    """Creates a check for each part of the extraction process to ensure the correct amount of data is gathered from the original annotation file.
        The unique argument is the contig to search for within the annotation file.
        The annotation argument is the original annotaiton file"""
    contig = re.compile(ur'(%s)'%(unique))
    length = contig.findall(annotation)
    length_checker = len(length)
    print length_checker
    return(length_checker)


#   Build the GFF file
def gff3_builder(outfile, contig_pseudo, source, types, start, end, score, strand, phase, attributes, length_checker):
    """Builds a GFF file from extracted components of original GFF file"""
    gff= open(outfile, 'w')
    print "opened " + outfile + " for writing"
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


#   Do the work here
def gff_to_gff(lock, seq_list, unique, reference, annotation, pseudoscaffold, outfile):
    """Extract information from original annotation file and match it up to sequences defined in pseudoscaffold. Then build a GFF annotation using this data for the pseudoscaffold"""
#    lock.acquire()
    length_checker = find_length(unique, annotation)
    sources = gff_extracter.source_finder(unique, annotation, length_checker)
    types = gff_extracter.type_finder(unique, annotation, length_checker)
    scores = gff_extracter.score_finder(unique, annotation, length_checker)
    strands = gff_extracter.strandedness(unique, annotation, length_checker)
    phases = gff_extracter.phase_finder(unique, annotation, length_checker)
    attributes = gff_extracter.attribute_finder(unique, annotation, length_checker)
    extracted_sequence = pseudoscaffold_tools.sequence_extracter(seq_list, unique)
    contig_pseudo = pseudoscaffold_tools.contig_finder(extracted_sequence, length_checker, pseudoscaffold)
    start, end = pseudoscaffold_tools.length_gff(extracted_sequence, length_checker, pseudoscaffold)
    gff3_builder(outfile, contig_pseudo, sources, types, start, end, scores, strands, phases, attributes, length_checker)
#    lock.release()
