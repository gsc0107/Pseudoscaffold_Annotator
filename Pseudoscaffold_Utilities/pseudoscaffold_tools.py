#!/usr/bin/env python

"""A script to find information from the pseudoscaffold being annotated"""

#   Import required modules from standard Python library
import re
import sys


#       Find the seqid (column 1) from the GFF or BED file
def contig_extracter(annotation):
    """Extract the contig IDs from the original annotation file. Also provides one last check to make sure all information was transfered from original annotation file to annotation file for pseudoscaffold"""
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
    print("There are " + str(len(contig_original)) + " contigs to work with")
    return(contig_original, length_checker)


#      Extract the sequences defined by the original annotation file
def sequence_finder(seq_list, unique):
    """Find the sequences pertaining to the unique contig"""
    print("Searching for sequences unique to " + unique)
    sequence = re.compile(ur'(>%s:.*\n[ACTGN]+)'%(unique))
    finder = sequence.findall(seq_list)
    specific_filename = str(unique+'_sequence.fasta')
    specific_sequences = open(specific_filename, 'w')
    for i in range(len(finder)):
        specific_sequences.write(finder[i])
        specific_sequences.write("\n")
    specific_sequences.close()
    print("Found unique sequences")
    return(specific_filename)


#       Change start and end positions to match BED format
def length_bed(extracted_sequence, length_checker, pseudoscaffold):
    """ Not yet implemented"""
    pass
