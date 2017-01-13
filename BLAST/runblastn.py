#!/usr/bin/env python3

"""A script to hold functions utilizing NCBI's BLAST+"""

import sys
if sys.version_info.major is not 3:
    sys.exit("Please use Python 3 for this module: " + __name__)

import os
import re

#   Import required functions from the BioPython module
try:
    from typeguard import check_argument_types, typechecked
    from overload import overload
    from Bio.Blast.Applications import NcbiblastnCommandline
    # from Bio.Blast import NCBIXML
except ImportError as error:
    sys.exit("Failed to find " + error.name)


#   A custom error
class BLASTFailedError(Exception):
    """BLAST seems to have failed..."""


#   Another custom error
class MalformedConfigError(Exception):
    """The BLAST config file isn't formed correctly"""


#   Ensure we have our BLAST database
def validate_db(db_path: str) -> None:
    """Find a BLAST nucleotide database"""
    assert check_argument_types()
    db_name = os.path.basename(db_path)
    nhr = re.compile(r'(%s\.[0-9\.]*nhr)' % db_name).search
    nin = re.compile(r'(%s\.[0-9\.]*nin)' % db_name).search
    nsq = re.compile(r'(%s\.[0-9\.]*nsq)' % db_name).search
    nal = re.compile(r'(%s\.*nal)' % db_name).search
    db_directory = os.path.abspath(os.path.realpath(os.path.dirname(db_path)))
    if not db_directory:
        db_directory = os.getcwd()
    print('Searching for proper database files for', db_name, 'in', db_directory, file=sys.stderr)
    db_contents = '\n'.join(os.listdir(db_directory))
    if not nhr(db_contents) and not nin(db_contents) and not nsq(db_contents) and not nal(db_contents):
        raise FileNotFoundError("Failed to find the BLAST nucleotide database at " + db_path)


@overload
def run_blastn(cline: NcbiblastnCommandline, keep_query: bool=True):
    """Run BLASTn"""
    assert check_argument_types()
    print(cline, file=sys.stderr)
    cline()
    if not os.path.exists(cline.out):
        raise BLASTFailedError
    if not keep_query:
        os.remove(cline.query)
    return cline.out


@run_blastn.add
def run_blastn(query: str, database: str, evalue: float, max_hits: int, max_hsps: int, identity: float, keep_query: bool):
    """Run BLASTn"""
    assert check_argument_types()
    #   Create an output name
    print("Running BLAST with database:", database, file=sys.stderr)
    query_base = os.path.basename(os.path.splitext(query)[0])
    db_base = os.path.basename(os.path.splitext(database)[0])
    blast_out = os.getcwd() + '/' + query_base + '_' + db_base + '_BLAST.xml'
    #   Setup BLASTn
    blastn = NcbiblastnCommandline(
        query=query,
        db=database,
        evalue=evalue,
        outfmt=5,
        max_target_seqs=max_hits,
        max_hsps=max_hsps,
        perc_identity=identity,
        out=blast_out
    )
    #   Run BLASTn
    outfile = run_blastn(cline=blastn, keep_query=keep_query)
    return outfile


@run_blastn.add
@typechecked
def run_blastn(bconf: dict) -> str:
    """Run BLASTn"""
    try:
        database = bconf['database']
        query = bconf['query']
        evalue = bconf['evalue']
        max_hits = bconf['max_hits']
        max_hsps = bconf['max_hsps']
        identity = bconf['identity']
        keep_query = bconf['keep_query']
        blast_out = run_blastn(
            query=query,
            database=database,
            evalue=evalue,
            max_hits=max_hits,
            max_hsps=max_hsps,
            identity=identity,
            keep_query=keep_query
        )
        return blast_out
    except KeyError:
        raise MalformedConfigError
    except:
        raise


#   Create BLAST config file
# def make_blast_config(args):
#     """Create a BLAST configuration file using settings defined by the user"""
#     import configparser
#     #   Get the name of the config file
#     #       and remove from the dictionary
#     #       of commands to be included in
#     #       the BLAST configuration
#     config_file = args.pop('config')
#     #   Remove the 'command' value from
#     #       the dictionary of commands to
#     #       be included in the BLAST configuration
#     args.pop('command')
#     #   Was a name for the blast database specified?
#     #   If not, remove it from the dictionary
#     if not args['db_name']:
#         args.pop('db_name')
#     #   Was a name for the blast database specified?
#     #   If not, remove it from the dictionary
#     if not args['outfile']:
#         args.pop('outfile')
#     #   Iterate through the dictionary
#     args_iterations = args.iteritems()
#     #   Setup the configuration parser
#     blast_config = configparser.RawConfigParser()
#     blast_config.add_section('BlastConfiguration')
#     #   Iterate through the dictionary and add to the config parser
#     try:
#         while True:
#             current_args = args_iterations.next()
#             blast_config.set('BlastConfiguration', current_args[0], current_args[1])
#     except StopIteration:
#         #   Write the configurations from the parser to the config file
#         config = open(config_file, 'wb')
#         blast_config.write(config)
#         print("BLAST configuration file can be found at " + config_file)


#   Read BLAST config file
# def blast_config_parser(config_file):
#     """Read the BLAST configuration file and pass arguments to BLAST functions"""
#     import configparser
#     #   Setup the configuration parser
#     blast_config = configparser.ConfigParser()
#     #   Read the configuration file
#     blast_config.read(config_file)
#     #   Create a dictionary for config options
#     bconf = dict(blast_config.items('BlastConfiguration'))
#     #   Make sure 'override' is a boolean type, not a string type
#     bconf['override'] = blast_config.getboolean('BlastConfiguration', 'override')
#     print("BLAST configuration file has been read")
#     return(bconf)


#   Make a BLAST database
# def make_blast_database(bconf, shellpath, pseudoscaffold, pseudopath, temppath):
#     """Make a BLAST database from the pseudoscaffold using a shell script and NCBI's BLAST+ excecutables"""
#     import subprocess
#     #   Change to the directory containing the pseudoscaffold
#     os.chdir(pseudopath)
#     #   See if we are lacking a name for the database specified
#     if bconf.get('db_name') == None:
#         base = os.path.basename(pseudoscaffold)
#         database_name = base.split('.')[0]
#     #   Nope, we have
#     else:
#         database_name = bconf['db_name']
#     #   What was the override command?
#     override = bconf['override']
#     #   Do we make or not?
#     makebool = find_database(database_name, override)
#     database_type = 'nucl'
#     #   Yes
#     if makebool:
#         database_script = str(shellpath + '/make_blast_database.sh')
#         print("Making BLAST database")
#         database_cmd = ['bash', database_script, pseudoscaffold, database_name, database_type]
#         database_shell = subprocess.Popen(database_cmd, shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
#         out, err = database_shell.communicate()
#         print("Finished making BLAST database")
#     #   No
#     else:
#         out, err = 0, 0
#     os.chdir(temppath)
#     return(database_name, out, err)


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
# def blast_parser(blast_out, length_checker, temppath, unique_sequence, types):
#     """Parse the BLAST results, correcting for small sequences not found by BLAST"""
#     #   Set up lists to hold info extracted from BLAST search
#     iterations = list()
#     scaffolds = list()
#     starts = list()
#     ends = list()
#     #   Define the regex object for searching through the BLAST XML document
#     find_info = re.compile(r'<Iteration>\s{3}<Iteration_iter-num>(\d*)</Iteration_iter-num>\s{3}<Iteration_query-ID>\w*</Iteration_query-ID>\s{3}<Iteration_query-def>[\w\d:-]*</Iteration_query-def>\s{3}<Iteration_query-len>\d*</Iteration_query-len>\s{1}<Iteration_hits>\s{1}<Hit>[\w\W]*?<Hit_def>([\w\d]*)[\w\W]*?<Hsp_hit-from>([\d]*)[\w\W]*?<Hsp_hit-to>(\d*)')
#     #   Find all information in the BLAST XML document
#     blast_xml = open(blast_out).read()
#     extracted_info = find_info.findall(blast_xml)
#     #   Sort the extracted information into their respective lists
#     for info in range(len(extracted_info)):
#         hit = extracted_info[info]
#         iterations.append(hit[0])
#         scaffolds.append(hit[1])
#         starts.append(hit[2])
#         ends.append(hit[3])
#     #   Make sure we have everything
#     if not len(scaffolds) == length_checker or not len(starts) == length_checker or not len(ends) == length_checker:
#         num_missing = length_checker - len(iterations)
#         print("We have " + str(len(iterations)) + " hit(s) so far")
#         print("Missing " + str(num_missing) + " hit(s), searching now ...")
#         #   Convert iterations string from character to integers to a set
#         iterations = map(int, iterations)
#         #   Find the missing iterations
#         iterations = set(iterations)
#         #       Use the set.difference method to compare a sequence of numbers
#         #       representing the number of iterations that should have had to the
#         #       number of iterations that were actually found. Add one for Python.
#         #       This will give us the iteration(s) that failed.
#         missing_iters = list(set(range(1, length_checker + 1)).difference(iterations))
#         print("Missing iteration numbers:")
#         print(missing_iters)
#         #   Get the informaiton for the full gene
#         gene_info = gene_finder(types, extracted_info, blast_xml)
#         #   Find the contig definitions for each missing hit
#         sequence = open(temppath + '/' + unique_sequence).read()
#         for missing in missing_iters:
#             for gene_part in gene_info:
#                 query_searcher = re.compile(r'<Iteration>\s{3}<Iteration_iter-num>%s</Iteration_iter-num>\s{3}<Iteration_query-ID>\w*</Iteration_query-ID>\s{3}<Iteration_query-def>([\w\d:-]*)'%(str(missing)))
#                 query = query_searcher.search(blast_xml).groups()[0]
#                 #   Find the missing information from the original sequence file
#                 #   The sequence for the missing query for checking
#                 get_sequence = re.compile(r'>%s\s([ACGTN]*)'%(query))
#                 q_seq = get_sequence.search(sequence).groups()[0]
#                 print("Qseq: " + q_seq)
#                 #   Start and end positions for this query
#                 q_start = query.split(':')[1].split('-')[0]
#                 print("Qstart: " + q_start)
#                 q_end = query.split(':')[1].split('-')[1]
#                 print("Qend: " + q_end)
#                 #   Ensure the missing sequence exists within the gene sequence
#                 gene_seq = re.search(r'>%s\s([ACGTN]*)'%(gene_part[4]), sequence).groups()[0]
#                 print("Gene sequence: " + gene_seq)
#                 print(gene_part[5])
#                 print(gene_part[6])
#                 tstart = int(q_start) - int(gene_part[5])
#                 tend = int(q_end) - int(gene_part[6])
#                 if tend == 0:
#                     test_seq = gene_seq[tstart :]
#                 else:
#                     test_seq = gene_seq[int(q_start) - int(gene_part[5]) : int(q_end) - int(gene_part[6])]
#                 print("Test_seq: " + test_seq)
#                 if test_seq == q_seq:
#                     #   Scale the q_start and q_end values to match that of the pseudoscaffold
#                     q_start = int(gene_part[2]) - int(gene_part[5]) + int(q_start)
#                     q_end = int(gene_part[2]) - int(gene_part[5]) + int(q_end)
#                     #   Figure out where to insert the new information into existing lists
#                     insert_position = missing - 1
#                     iterations = list(iterations)
#                     iterations.insert(insert_position, missing)
#                     scaffolds.insert(insert_position, scaffolds[0])
#                     starts.insert(insert_position, str(q_start))
#                     ends.insert(insert_position, str(q_end))
#                     break
#                 else:
#                     print("Could not find " + q_seq + " in the gene sequence")
#                     print("Whoops")
#         if not len(scaffolds) == length_checker or not len(starts) == length_checker or not len(ends) == length_checker:
#             sys.exit("Failed to find missing hit(s)")
#         else:
#             print("Found the missing values")
#             return(scaffolds, starts, ends)
#     else:
#             print("Found all hits")
#             return(scaffolds, starts, ends)


#   Find the contigs that count as genes for fixing BLAST parsing
# def gene_finder(types, extracted_info, blast_xml):
#     """Find all genes defined by the annotation file"""
#     #   Create a list to store which entries are genes for this contig
#     gene_info = list()
#     #   Search for the genes using the 'types' list from earlier
#     for index, entry in enumerate(types):
#         if "gene" in entry:
#             fixed_index = index + 1
#             #   Find the sections defined from the 'extracted_info' list
#             for hit in extracted_info:
#                 if str(index + 1) == str(hit[0]):
#                     extracted_index = extracted_info.index(hit)
#                     break
#             gene_part = list(extracted_info[extracted_index])
#             gene_def = re.search(r'<Iteration>\s{3}<Iteration_iter-num>%s</Iteration_iter-num>\s{3}<Iteration_query-ID>\w*</Iteration_query-ID>\s{3}<Iteration_query-def>([\w\d:-]*)'%(str(fixed_index)), blast_xml).groups()[0]
#             gene_part.append(gene_def)
#             #Get the definintion start and ends of the gene
#             gene_part = gene_part + gene_part[4].split(':')[1].split('-')
#             gene_info.append(gene_part)
#     return(gene_info)


# #   Run the BLAST search and parse the results
# def run_blast(bconf, unique_sequence, database_name, length_checker, temppath, pseudopath, unique, types):
#     """Perform the BLAST search and parse the results"""
#     #   BLAST
#     blast_out = blast_search(bconf, unique_sequence, database_name, temppath, pseudopath, unique)
#     scaffolds, starts, ends = blast_parser(blast_out, length_checker, temppath, unique_sequence, types)
#     return(scaffolds, starts, ends)
