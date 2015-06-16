#!/usr/bin/env python

#   A script to find information from the pseudoscaffold being annotated
import re
import sys

#      Extract the sequences defined by the original annotation file
def sequence_extracter(seq_list, unique):
    """Extract the sequences as defined by the original annotation file.
        Both arguments are strings containing the names of the file. These files get passed to a shell script utilizing the BEDTools suite (not the BED_Tools module) to extract the sequences outlined by the annotation file from the reference FASTA file.

        These sequences get passed to other functions for determining the start and stop locations within the pseudoscaffold."""
    sequence = re.compile(ur'(?<=%s).*\n([ACTGN]+)'%unique)
    extracter = sequence.findall(seq_list)
    print("Found sequences")
    return(extracter)


#       Find the pseudoscaffold ID where the sequences are stored
def contig_finder(extracted_sequence, length_checker, pseudoscaffold):
    """Find the comparitive contigs for each sequence within pseudoscaffold.
        The extracted_sequence argument is the list sequences extracted from the reference FASTA file.
        The length_checker argument is the number of sequences that should be extracted.
        The pseudoscaffold argument is the read of the pseudoscaffold."""
    contig_pseudo = list()
    for captured in extracted_sequence:
        sequence_find = re.compile(ur'(^>[0-9a-z_\s]+)(?=\s.*%s)'%(captured), re.MULTILINE | re.DOTALL)
        ID = sequence_find.search(pseudoscaffold)
        contig_pseudo.append(ID.group())
    if len(contig_pseudo) == length_checker:
        print("Pseudoscaffold contigs found")
        return(contig_pseudo)
    else:
        sys.exit("Failed to find all pseudoscaffold contigs")


#       Calculate start and end positions within the pseudoscaffold for a GFF file
def length_gff(extracted_sequence, length_checker, pseudoscaffold):
    """Calculate the start and end positions for each sequence within the pseudoscaffold.
        The extracted_sequence argument is the list sequences extracted from the reference FASTA file.
        The length_checker argument is the number of sequences that should be extracted.
        The pseudoscaffold argument is the read of the pseudoscaffold."""
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


#       Calculate start and end posiotns within the pseudoscaffold for a BED file
def length_bed(extracted_sequence, length_checker, pseudoscaffold):
    """ Not yet implemented"""
    pass
