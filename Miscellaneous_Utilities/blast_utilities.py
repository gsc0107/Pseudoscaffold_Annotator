#!/usr/bin/env python

"""A script to hold functions utilizing NCBI's BLAST+"""

import sys
import os
import re

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
def find_database(database_name, override):
    """Determine if the resources are going to be spent making a BLAST database"""
    #   See if the file exists first
    #   The extension associated with the BLAST database
    ext = '.nin'
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
    #   What was the override command?
    override = bconf['override']
    #   Do we make or not?
    makebool = find_database(database_name, override)
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
        evalue=0.05,
        max_target_seqs=1,
        outfmt=5,
        out=blast_out)
    print("Running BLAST search")
    #   Run the BLAST search
    blastn_cline()
    print("Finished searching")
    os.chdir(temppath)
    return(blast_out)


#   A new BLAST parser that finds what we're looking for while correcting for sequences too small to be found by BLAST
def blast_parser(blast_out, length_checker, temppath, unique_sequence):
    """Parse the BLAST results, correcting for small sequences not found by BLAST"""
    #   Set up lists to hold info extracted from BLAST search
    iterations = list()
    scaffolds = list()
    starts = list()
    ends = list()
    #   Define the regex object for searching through the BLAST XML document
    find_info = re.compile(ur'<Iteration>\s{3}<Iteration_iter-num>(\d*)</Iteration_iter-num>\s{3}<Iteration_query-ID>\w*</Iteration_query-ID>\s{3}<Iteration_query-def>[\w\d:-]*</Iteration_query-def>\s{3}<Iteration_query-len>\d*</Iteration_query-len>\s{1}<Iteration_hits>\s{1}<Hit>[\w\W]*?<Hit_def>([\w\d]*)[\w\W]*?<Hsp_hit-from>([\d]*)[\w\W]*?<Hsp_hit-to>(\d*)')
    #   Find all information in the BLAST XML document
    blast_xml = open(blast_out).read()
    extracted_info = find_info.findall(blast_xml)
    #   Sort the extracted information into their respective lists
    for info in range(len(extracted_info)):
        hit = extracted_info[info]
        iterations.append(hit[0])
        scaffolds.append(hit[1])
        starts.append(hit[2])
        ends.append(hit[3])
    #   Make sure we have everything
    if not len(scaffolds) == length_checker or not len(starts) == length_checker or not len(ends) == length_checker:
        num_missing = length_checker - len(iterations)
        print("Missing " + str(num_missing) + " hit(s), searching now ...")
        #   Convert iterations string from character to integers to a set
        iterations = map(int, iterations)
        #   Find the missing iterations
        iterations = set(iterations)
        #       Use the set.difference method to compare a sequence of numbers
        #       representing the number of iterations that should have had to the
        #       number of iterations that were actually found.
        #       This will give us the iteration(s) that failed.
        missing_iters = list(set(range(1, length_checker)).difference(iterations))
        #   Get the informaiton for the full gene
        gene_info = list(extracted_info[0])
        gene_def = re.search(ur'<Iteration>\s{3}<Iteration_iter-num>1</Iteration_iter-num>\s{3}<Iteration_query-ID>\w*</Iteration_query-ID>\s{3}<Iteration_query-def>([\w\d:-]*)', blast_xml).groups()[0]
        gene_info.append(gene_def)
        #   Get the definintion start and ends of the gene
        gene_info = gene_info + gene_info[4].split(':')[1].split('-')
        #   Find the contig definitions for each missing hit
        sequence = open(temppath + '/' + unique_sequence).read()
        for missing in missing_iters:
            query_searcher = re.compile(ur'<Iteration>\s{3}<Iteration_iter-num>%s</Iteration_iter-num>\s{3}<Iteration_query-ID>\w*</Iteration_query-ID>\s{3}<Iteration_query-def>([\w\d:-]*)'%(str(missing)))
            query = query_searcher.search(blast_xml).groups()[0]
            #   Find the missing information from the original sequence file
            #   The sequence for the missing query for checking
            get_sequence = re.compile(ur'>%s\s([ACGTN]*)'%(query))
            q_seq = get_sequence.search(sequence).groups()[0]
            #   Start and end positions for this query
            q_start = query.split(':')[1].split('-')[0]
            q_end = query.split(':')[1].split('-')[1]
            #   Ensure the missing sequence exists within the gene sequence
            gene_seq = re.search(ur'>%s\s([ACGTN]*)'%(gene_info[4]), sequence).groups()[0]
            test_seq = gene_seq[int(q_start) - int(gene_info[5]) : int(q_end) - int(gene_info[6])]
            if test_seq == q_seq:
                #   Scale the q_start and q_end values to match that of the pseudoscaffold
                q_start = int(gene_info[2]) - int(gene_info[5]) + int(q_start)
                q_end = int(gene_info[2]) - int(gene_info[5]) + int(q_end)
                #   Figure out where to insert the new information into existing lists
                insert_position = missing - 1
                iterations = list(iterations)
                iterations.insert(insert_position, missing)
                scaffolds.insert(insert_position, scaffolds[0])
                starts.insert(insert_position, str(q_start))
                ends.insert(insert_position, str(q_end))
            else:
                sys.exit("Failed to find missing hit")
        if not len(scaffolds) == length_checker or not len(starts) == length_checker or not len(ends) == length_checker:
            sys.exit("Failed to find missing hit")
        else:
            return(scaffolds, starts, ends)
    else:
            print("Found all hits")
            return(scaffolds, starts, ends)
    # return(queries)


#   Run the BLAST search and parse the results
def run_blast(bconf, unique_sequence, database_name, length_checker, temppath, pseudopath, unique):
    """Perform the BLAST search and parse the results"""
    #   BLAST
    blast_out = blast_search(bconf, unique_sequence, database_name, temppath, pseudopath, unique)
    scaffolds, starts, ends = blast_parser(blast_out, length_checker, temppath, unique_sequence)
    print len(scaffolds)
    print len(starts)
    print len(ends)
    return(scaffolds, starts, ends)
