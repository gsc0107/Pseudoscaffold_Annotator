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


#   Create BLAST config file
def make_blast_config(args):
    """Create a BLAST configuration file using settings defined by the user"""
    import ConfigParser
    config_file = args.pop('config')
    args.pop('command')
    if not args['db_name']:
        args.pop('db_name')
    if not args['outfile']:
        args.pop('outfile')
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
        print("BLAST configuration file can be found at " + config_file)


#   Read BLAST config file
def blast_config_parser(config_file):
    """Read the BLAST configuration file and pass arguments to BLAST functions"""
    import ConfigParser
    blast_config = ConfigParser.ConfigParser()
    blast_config.read(config_file)
    bconf = dict(blast_config.items('BlastConfiguration'))
    print("BLAST configuration file has been read")
    return(bconf)


#   Make a BLAST database
def make_blast_database(bconf, shellpath, pseudoscaffold):
    """Make a BLAST database from the pseudoscaffold using a shell script and NCBI's BLAST+ excecutables"""
    import subprocess
    if bconf.get('db_name') == None:
        database_name = os.path.basename(pseudoscaffold)
    else:
        database_name = bconf['db_name']
    database_type = bconf['db_type']
    if database_type == 'nucl':
        ext = '.nin'
    elif database_type == 'prot':
        ext = '.pin'
    else:
        sys.exit("Incorrect BLAST database type specified")
    print database_type
    override = bconf['override']
    database_script = str(shellpath + '/make_blast_database.sh')
    print("Making BLAST database")
    database_cmd = ['bash', database_script, pseudoscaffold, database_name, database_type, ext, override]
    database_shell = subprocess.Popen(database_cmd, shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = database_shell.communicate()
    print("Finished making BLAST database")
    return(database_name, out, err)


#   Define the BLAST program
def blast_search(bconf, unique_sequence, database_name, temppath):
    """Run BLASTN to find sequences within the pseudoscaffold"""
    if bconf.get('outfile') == None:
        blast_out = temppath + '/temp.xml'
    else:
        blast_out = bconf['outfile']
    blastn_cline = NcbiblastnCommandline(
        query=unique_sequence,
        db=database_name,
        evalue=bconf['evalue'],
        max_target_seqs=bconf['max_seqs'],
        outfmt=bconf['outfmt'],
        out=blast_out)
    print("Running BLAST search")
    blastn_cline()
    print("Finished searching")
    return(blast_out)


#   Parse the BLAST output
def blast_parser(bconf, blast_out):
    """Parse the BLAST results"""
    result_handle = open(blast_out)
    threshold = bconf['threshold']
    titles = list()
    starts = list()
    ends = list()
    blast_records = NCBIXML.parse(result_handle)
    print("Parsing BLAST results")
    try:
        while True:
            brecord = next(blast_records)
            for alignment in brecord.alignments:
                for hsp in alignment.hsps:
                    if hsp.expect < threshold:
                        titles.append(alignment.title)
                        starts.append(hsp.sbjct_start)
                        ends.append(hsp.sbjct_end)
                    break
    except StopIteration:
        print("Finished parsing results")
        return(titles, starts, ends)


#   Fix the titles of the hits, because NCBI's XML format is weird
def title_fixer(titles):
    print("Fixing titles from parsing BLAST results")
    fixed_titles = list()
    for i in range(len(titles)):
        title = titles[i]
        split_title = title.split()
        pseudo_contig = split_title[0]
        fixed_titles.append(pseudo_contig)
    print("Finished fixing titles")
    return(fixed_titles)

#   Run the BLAST search and parse the results
def run_blast(bconf, unique_sequence, database_name, length_checker, temppath):
    blast_out = blast_search(bconf, unique_sequence, database_name, temppath)
    titles, starts, ends = blast_parser(bconf, blast_out)
    fixed_titles = title_fixer(titles)
    if not len(fixed_titles) == length_checker or not len(starts) == length_checker or not len(ends) == length_checker:
        sys.exit("Failed to find all sequences in BLAST search")
    else:
        return(fixed_titles, starts, ends)

#   Find matches from BLAST search
# def blast_match():
#     import subprocess
#     matching_script = str(shellpath + '/blast_database_sequence.sh')
#     matching_cmd = ['bash', matching_script]
#     matching_shell = subprocess.Popen(matching_cmd, shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
#     out, err = matching_shell.communicate()
#     return(out, err)
