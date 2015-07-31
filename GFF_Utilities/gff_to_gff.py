#!/usr/bin/env python

"""A script to build a GFF annotation with a reference GFF file"""

#   Import required modules from standard Python library
import re
import os

#   Import functions defined in another script bundled with this package
import Pseudoscaffold_Utilities.pseudoscaffold_tools as pseudoscaffold_tools
import Miscellaneous_Utilities.blast_utilities as blast_utilities
import gff_extracter


#   Find the number of times this a contig shows up in original annotation file
def find_length(unique, annotation):
    """Creates a check for each part of the extraction process to ensure the correct amount of data is gathered from the original annotation file.
        The unique argument is the contig to search for within the annotation file.
        The annotation argument is the original annotation file"""
    contig = re.compile(ur'(%s)\t'%(unique))
    length = contig.findall(annotation)
    length_checker = len(length)
    print("There should be " + str(length_checker) + " sequences")
    return(length_checker)


#   Build the GFF file
def gff3_builder(titles, sources, types, starts, ends, scores, strands, phases, attributes, length_checker, outfile):
    """Builds a GFF file from extracted components of original GFF file"""
    gff= open(outfile, 'w')
    print("Opened " + outfile + " for writing")
    for i in range(0, length_checker):
        gff.write(str(titles[i]))
        gff.write('\t')
        gff.write(str(sources[i]))
        gff.write('\t')
        gff.write(str(types[i]))
        gff.write('\t')
        gff.write(str(starts[i]))
        gff.write('\t')
        gff.write(str(ends[i]))
        gff.write('\t')
        gff.write(str(scores[i]))
        gff.write('\t')
        gff.write(str(strands[i]))
        gff.write('\t')
        gff.write(str(phases[i]))
        gff.write('\t')
        gff.write(str(attributes[i]))
        gff.write('\n')
        gff.close()
    print("GFF file created")
    return


#   Do the work here
def gff_to_gff(seq_list, unique, annotation, pseudoscaffold, outfile, temppath, bconf, database_name, pseudopath):
    """Extract information from original annotation file and match it up to sequences defined in pseudoscaffold. Then build a GFF annotation using this data for the pseudoscaffold"""
    print("Working on finding " + unique + " in the pseudoscaffold")
    if not os.getcwd() == temppath:
        os.chdir(temppath)
    length_checker = find_length(unique, annotation)
    sources = gff_extracter.source_finder(unique, annotation, length_checker)
    types = gff_extracter.type_finder(unique, annotation, length_checker)
    scores = gff_extracter.score_finder(unique, annotation, length_checker)
    strands = gff_extracter.strandedness(unique, annotation, length_checker)
    phases = gff_extracter.phase_finder(unique, annotation, length_checker)
    attributes = gff_extracter.attribute_finder(unique, annotation, length_checker)
    unique_sequences = pseudoscaffold_tools.sequence_finder(seq_list, unique)
    titles, starts, ends = blast_utilities.run_blast(bconf, unique_sequences, database_name, length_checker, temppath, pseudopath, unique, types)
    gff3_builder(titles, sources, types, starts, ends, scores, strands, phases, attributes, length_checker, outfile)
    return
