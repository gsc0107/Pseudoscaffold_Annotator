#!/usr/bin/env python

#   A script to find information from the pseudoscaffold being annotated
import subprocess
import re
import sys

#      Extract the sequences defined by the original annotation file
def sequence_extracter(reference, annotation):
    tmp = 'pseudoscaffold_annotator_temp.fasta'
    print("Searching for original sequences using 'extraction.sh'")
    extraction_cmd = ['bash', './Shell_Scripts/extraction.sh', reference, annotation, tmp]
    extraction_shell = subprocess.Popen(extraction_cmd, shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = extraction_shell.communicate()
    seq_list = open(tmp).read()
    sequence = re.compile(ur'([ACTGN]+)')
    extracter = sequence.findall(seq_list)
    #os.remove(tmp)
    print("Found sequences")
    return(extracter)


#       Find the pseudoscaffold ID where the sequences are stored
def contig_finder(extracted_sequence, length_checker, pseudoscaffold):
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
    pass
