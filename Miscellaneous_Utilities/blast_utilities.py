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
    #   Get the name of the config file
    #       and remove from the dictionary
    #       of commands to be included in
    #       the BLAST configuration
    config_file = args.pop('config')
    #   Remove the 'command' value from
    #       the dictionary of commands to
    #       be included in the BLAST configuration
    args.pop('command')
    #   Was a name for the blast database specified?
    #   If not, remove it from the dictionary
    if not args['db_name']:
        args.pop('db_name')
    #   Was a name for the blast database specified?
    #   If not, remove it from the dictionary
    if not args['outfile']:
        args.pop('outfile')
    #   Iterate through the dictionary
    args_iterations = args.iteritems()
    #   Setup the configuration parser
    blast_config = ConfigParser.RawConfigParser()
    blast_config.add_section('BlastConfiguration')
    #   Iterate through the dictionary and add to the config parser
    try:
        while True:
            current_args = args_iterations.next()
            blast_config.set('BlastConfiguration', current_args[0], current_args[1])
    except StopIteration:
        #   Write the configurations from the parser to the config file
        config = open(config_file, 'wb')
        blast_config.write(config)
        print("BLAST configuration file can be found at " + config_file)


#   Read BLAST config file
def blast_config_parser(config_file):
    """Read the BLAST configuration file and pass arguments to BLAST functions"""
    import ConfigParser
    #   Setup the configuration parser
    blast_config = ConfigParser.ConfigParser()
    #   Read the configuration file
    blast_config.read(config_file)
    #   Create a dictionary for config options
    bconf = dict(blast_config.items('BlastConfiguration'))
    #   Make sure 'override' is a boolean type, not a string type
    bconf['override'] = blast_config.getboolean('BlastConfiguration', 'override')
    print("BLAST configuration file has been read")
    return(bconf)


#   Determine whether or not we're making a new BLAST database
def find_database(database_name, ext, override):
    """Determine if the resources are going to be spent making a BLAST database"""
    #   See if the file exists first
    if os.path.isfile(database_name + ext):
        print("Existing BLAST database found")
        #   If so, can we override?
        if override:
            print("Override set to 'True'")
            makebool = True
        #   Or not?
        else:
            print ("Override set to 'False'")
            makebool = False
    #   Guess the file doesn't exist...
    else:
        print("Could not find existing BLAST database")
        makebool = True
    return makebool


#   Make a BLAST database
def make_blast_database(bconf, shellpath, pseudoscaffold, pseudopath, temppath):
    """Make a BLAST database from the pseudoscaffold using a shell script and NCBI's BLAST+ excecutables"""
    import subprocess
    #   Change to the directory containing the pseudoscaffold
    os.chdir(pseudopath)
    #   See if we are lacking a name for the database specified
    if bconf.get('db_name') == None:
        base = os.path.basename(pseudoscaffold)
        database_name = base.split('.')[0]
    #   Nope, we have
    else:
        database_name = bconf['db_name']
    #   What kind of BLAST database do we have?
    database_type = bconf['db_type']
    #   What is the extension associated with the BLAST database?
    if database_type == 'nucl':
        ext = '.nin'
    elif database_type == 'prot':
        ext = '.pin'
    else:
        sys.exit("Incorrect BLAST database type specified")
    #   What was the override command?
    override = bconf['override']
    #   Do we make or not?
    makebool = find_database(database_name, ext, override)
    #   Yes
    if makebool:
        database_script = str(shellpath + '/make_blast_database.sh')
        print("Making BLAST database")
        database_cmd = ['bash', database_script, pseudoscaffold, database_name, database_type]
        database_shell = subprocess.Popen(database_cmd, shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = database_shell.communicate()
        print("Finished making BLAST database")
    #   No
    else:
        out, err = 0, 0
    os.chdir(temppath)
    return(database_name, out, err)


#   Define the BLAST program
def blast_search(bconf, unique_sequence, database_name, temppath, pseudopath, unique):
    """Run BLASTN to find sequences within the pseudoscaffold"""
    #   Change do directory containing pseudoscaffold
    os.chdir(pseudopath)
    #   Are we lacking an outfile for BLAST results?
    if bconf.get('outfile') == None:
        blast_out = temppath + '/' + unique + '_temp.xml'
    #   Nope, we got
    else:
        blast_out = bconf['outfile']
    #   Where is the query file?
    unique_query = temppath + '/' + unique_sequence
    #   Define the BLAST search
    blastn_cline = NcbiblastnCommandline(
        query=unique_query,
        db=database_name,
        evalue=bconf['evalue'],
        max_target_seqs=bconf['max_seqs'],
        outfmt=bconf['outfmt'],
        out=blast_out)
    print("Running BLAST search")
    #   Run the BLAST search
    blastn_cline()
    print("Finished searching")
    os.chdir(temppath)
    return(blast_out)


#   Parse the BLAST output
def blast_parser(bconf, blast_out):
    """Parse the BLAST results"""
    #   Open the BLASt results
    result_handle = open(blast_out)
    #   What's out threshold value?
    threshold = bconf['threshold']
    #   Set up lists to hold our output
    titles = list()
    starts = list()
    ends = list()
    #   Parse the BLAST results
    print("Parsing BLAST results")
    blast_records = NCBIXML.parse(result_handle)
    #   Iterate through the BLAST results
    #       getting the title, start,
    #       and end of each sequence
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
    """Remove the excess informaiton from the 'title' field from the XML resutls"""
    print("Fixing titles from parsing BLAST results")
    #   Set up a new list for fixing the titles
    fixed_titles = list()
    #   Fix the titles
    for i in range(len(titles)):
        title = titles[i]
        split_title = title.split()
        pseudo_contig = split_title[0]
        fixed_titles.append(pseudo_contig)
    print("Finished fixing titles")
    return(fixed_titles)

#   Run the BLAST search and parse the results
def run_blast(bconf, unique_sequence, database_name, length_checker, temppath, pseudopath, unique):
    """Perform the BLAST search and parse the results"""
    #   BLAST
    blast_out = blast_search(bconf, unique_sequence, database_name, temppath, pseudopath, unique)
    titles, starts, ends = blast_parser(bconf, blast_out)
    fixed_titles = title_fixer(titles)
    print len(titles)
    print len(fixed_titles)
    print len(starts)
    print len(ends)
    if not len(fixed_titles) == length_checker or not len(starts) == length_checker or not len(ends) == length_checker:
        sys.exit("Failed to find all sequences in BLAST search")
    else:
        return(fixed_titles, starts, ends)
