#!/usr/bin/env python

"""A script to hold functions utilizing NCBI's BLAST+"""

import sys

#   Import required functions from the BioPython module
try:
    from Bio.Blast.Applications import NcbiblastnCommandline
    from Bio.Blast import NCBIXML
except ImportError:
    sys.exit("Please install BioPython")


#   Make a BLAST database
def make_blast_database(rootpath, pseudoscaffold):
    import subprocess
    database_name = ''
    database_script = str(rootpath + 'Shell_Scripts/make_blast_database.sh')
    database_cmd = ['bash', database_script, pseudoscaffold, database_name]
    database_shell = subprocess.Popen(database_cmd, shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = database_shell.communicate()
    return(database_name, out, err)


#   Define the BLAST program
def run_blast(sequence, blast_settings, ):
    blastn_cline = NcbiblastnCommandline()
    blastn_cline()


#   Parse the BLAST output
def blast_parser():
    result_handle = open()
    blast_records = NCBIXML.parse(result_handle)
    blast_record = next(blast_records)
    try:
        while True:
            blast_record = next(blast_records)
    except StopIteration:
            pass
    parse_results = open()
    for alignment in blast_record.alignments:
        for hsp in alignment.hsps:
            if hsp.expect < threshold:
                pass


#   Find matches from BLAST search
def blast_match():
    import subprocess
    matching_script = str(rootpath + 'Shell_Scripts/blast_database_sequence.sh')
    matching_cmd = ['bash', matching_script]
    matching_shell = subprocess.Popen(matching_cmd, shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = matching_shell.communicate()
