#!/usr/bin/env python

"""A script to hold functions utilizing NCBI's BLAST+"""

import sys
import os

#   Import required functions from the BioPython module
try:
    from Bio.Blast.Applications import NcbiblastnCommandline
    from Bio.Blast import NCBIXML
except ImportError:
    sys.exit("Please install BioPython and put in your PythonPath")


#   Make a BLAST database
def make_blast_database(rootpath, pseudoscaffold):
    """Make a BLAST database from the pseudoscaffold using a shell script and NCBI's BLAST+ excecutables"""
    import subprocess
    database_name = os.path.basename(pseudoscaffold)
    database_script = str(rootpath + 'Shell_Scripts/make_blast_database.sh')
    database_cmd = ['bash', database_script, pseudoscaffold, database_name]
    database_shell = subprocess.Popen(database_cmd, shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = database_shell.communicate()
    return(database_name, out, err)


#   Create BLAST config file
def make_blast_config(args):
    """Create a BLAST configuration file using settings defined by the user"""
    import ConfigParser
    config_file = args.pop('config')
    args.pop('command')
    args_iterations = args.iteritems()
    blast_config = ConfigParser.RawConfigParser()
    blast_config.add_section('BlastConfiguration')
    try:
        while True:
            current_args = args_iterations.next()
            blast_config.set('BlastConfiguration', current_args[0], current_args[1])
    except StopIteration:
        config = open(config_file, 'wb')
        blast_config.write(config)
    test_reader = open(config_file).read()
    print(test_reader)


#   Read BLAST config file
def blast_config_parser(config_file):
    """Read the BLAST configuration file and pass arguments to BLAST functions"""
    import ConfigParser
    blast_config = ConfigParser.ConfigParser()
    pass


#   Define the BLAST program
def run_blast(sequence, database_name):
    """Run BLASTN to find sequences within the pseudoscaffold"""
    blast_out = ''
    blastn_cline = NcbiblastnCommandline(
        query=sequence,
        db=database_name,
        evalue=evalue,
        max_target_seqs=max_seqs,
        outfmt=5,
        out=blast_out)
    blastn_cline()
    return(blast_out)


#   Parse the BLAST output
def blast_parser():
    """Parse the BLAST results"""
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
                start = hsp.sbjt_start


#   Find matches from BLAST search
def blast_match():
    import subprocess
    matching_script = str(rootpath + 'Shell_Scripts/blast_database_sequence.sh')
    matching_cmd = ['bash', matching_script]
    matching_shell = subprocess.Popen(matching_cmd, shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = matching_shell.communicate()
    return(out, err)
