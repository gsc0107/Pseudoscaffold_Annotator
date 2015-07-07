#!/usr/bin/env python

#   Import required modules from standard Python library
import argparse
import os


#   Set rootpath to current working directory
rootpath = os.getcwd()

#   Set and parse arguments
def set_args():
    """Set and parse the arguments here. There are three subroutines for this package:
        fix             Fix a pseudoscaffold file to be used by the annotator
        blast-config    Set the default arguments for BLAST to be used by the annotator
        annotate        Run the annotator itself"""
    #   Define the arguments
    Arguments = argparse.ArgumentParser(add_help=True)
    Sub_Args = Arguments.add_subparsers(help='Choose what to do', dest='command')
    #   Add parser for fixing pseudoscaffold
    Fix_Arguments = Sub_Args.add_parser('fix', help='Fix an input pseudoscaffold for use with the annotator')
    Fix_Arguments.add_argument('-p',
        '--pseudoscaffold',
        type=str,
        default=None,
        metavar='PSEUDOSCAFFOLD FASTA',
        help="Pseudoscaffold to be annotated")
    Fix_Arguments.add_argument('-n',
        '--new-pseudoscaffold',
        type=str,
        default='fixed_pseudoscaffolds.fasta',
        metavar='FIXED PSEUDOSCAFFOLD',
        help="Name of fixed pseudoscaffold. Please put full file name, inlcuding extension. Default is 'fixed_pseudoscaffolds.fasta'")
    #   Add parser for setting BLAST defaults
    Blast_Arguments = Sub_Args.add_parser('blast-config', help='Set defaults for BLAST to be used by the annotator')
    Blast_Arguments.add_argument('-e',
        '--evalue',
        type=float,
        default=0.05,
        metavar='EVALUE',
        help="Evalue for BLAST search, default is 0.05")
    Blast_Arguments.add_argument('-m',
        '--max_seqs',
        type=float,
        default=5,
        metavar='MAX TARGET SEQUENCES',
        help="Maximum number of target sequences for BLAST search, default is 5")
    Blast_Arguments.add_argument('-c',
        '--config',
        metavar='BLAST CONFIG FILE',
        default=rootpath+'/blast_config',
        help="Full path to the BLAST configuration file. Defaults to "+rootpath+"/blast_config")
    #   Add parser for the annotator
    Annotate_Arguments = Sub_Args.add_parser('annotate', help='Annotate an input pseudoscaffold')
    Annotate_Arguments.add_argument('-r',
        '--reference',
        type=str,
        default=None,
        metavar='REFERENCE FASTA',
        help="Input reference FASTA file")
    Annotate_Arguments.add_argument('-a',
        '--annotation',
        type=str,
        default=None,
        metavar='ANNOTATION',
        help="Annotation file for reference FASTA")
    Annotate_Arguments.add_argument('-p',
        '--pseudoscaffold',
        type=str,
        default=None,
        metavar='PSEUDOSCAFFOLD FASTA',
        help="Pseudoscaffold to be annotated")
    Annotate_Arguments.add_argument('-o',
        '--outfile',
            type=str,
        default='pseudoscaffold_annotations.gff',
        metavar='OUTFILE',
        help="Desired name of output annotation file. Please put full file name, including extension. Defalt is 'pseudoscaffold_annotations.gff'")
    Annotate_Arguments.add_argument('-c',
        '--config',
        metavar='BLAST CONFIG FILE',
        default=rootpath+'/blast_config',
        help="Full path the BLAST configuration file. ")
    #   Parse the arguments
    args = Arguments.parse_args()
    return(args)


#   Usage message
def Usage():
    """Prints usage message"""
    print'''Usage: Pseudoscaffold_Annotator.py -r | --reference <reference fasta> -a | --annotation <reference annotation file> -p | --pseudoscaffold <assembled pseudoscaffold fasta> -o | --outfile <name of output annotation file>

Pseudoscaffold_Annotator.py creates a GFF annotation file
for an assembled pseudoscaffold fasta file based off a
reference fasta file and GFF annotation file for the
reference fasta file. Support for the BED format
will be included in a later release.

This program requires bedtools to be installed and
found within the system path. Please do this before
running Pseudscaffold_Annotator.py

***IMPORTANT***
Pseudoscaffold_Annotator.py requires no new lines
within the sequence of the pseudoscaffold.
The following is not an allowed sequence:
        >pseudoscaffold
        ACTGTCAG
        GCTATCGA

pseudoscaffold_fixer.py removes new lines
between sequence data, creating a fasta
file that reads like:
        >pseudoscaffold
        ACTGTCAGGCTATCGA
'''
    return
