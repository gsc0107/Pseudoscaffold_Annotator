#!/usr/bin/env python

"""A script to find information from the pseudoscaffold being annotated"""

#   Import required modules from standard Python library
import re
import sys

#      Extract the sequences defined by the original annotation file
def sequence_finder(seq_list, unique):
    """Find the sequences pertaining to the unique contig"""
    sequence = re.compile(ur'(>%s.*\n[ACTGN]+)'%(unique))
    finder = sequence.findall(seq_list)
    specific_filename = str(unique+'_sequence.fasta')
    specific_sequences = open(specific_filename, 'w')
    for i in range(len(finder)):
        specific_sequences.write(finder[i])
        specific_sequences.write("\n")
    specific_sequences.close()
    return(specific_filename)


#       Change start and end positions to match BED format
def length_bed(extracted_sequence, length_checker, pseudoscaffold):
    """ Not yet implemented"""
    pass
