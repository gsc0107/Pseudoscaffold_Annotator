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

#       Find the pseudoscaffold ID where the sequences are stored
# def contig_finder(extracted_sequence, length_checker, pseudoscaffold):
#     """Find the comparitive contigs for each sequence within pseudoscaffold.
#         The extracted_sequence argument is the list sequences extracted from the reference FASTA file.
#         The length_checker argument is the number of sequences that should be extracted.
#         The pseudoscaffold argument is the read of the pseudoscaffold."""
#     contig_pseudo = list()
#     for captured in extracted_sequence:
#         sequence_find = re.compile(ur'(^>[0-9a-z_\s]+)(?=\s.*%s)'%(captured), re.MULTILINE | re.DOTALL)
#         ID = sequence_find.search(pseudoscaffold)
#         contig_pseudo.append(ID.group())
#     if len(contig_pseudo) == length_checker:
#         print("Pseudoscaffold contigs found")
#         return(contig_pseudo)
#     else:
#         sys.exit("Failed to find all pseudoscaffold contigs")


#       Calculate start and end positions within the pseudoscaffold for a GFF file
# def length_gff(extracted_sequence, length_checker, pseudoscaffold):
#     """Calculate the start and end positions for each sequence within the pseudoscaffold.
#         The extracted_sequence argument is the list sequences extracted from the reference FASTA file.
#         The length_checker argument is the number of sequences that should be extracted.
#         The pseudoscaffold argument is the read of the pseudoscaffold."""
#     start = list()
#     end = list()
#     for extract in extracted_sequence:
#         start_value = pseudoscaffold.find(extract)+1
#         start.append(start_value)
#         end_value = start_value+len(extract)
#         end.append(end_value)
#     if len(start) == len(end) == length_checker:
#         print("All lengths calculated")
#         return(start, end)
#     else:
#         sys.exit("Failed to calculate all lengths")
