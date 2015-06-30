#!/usr/bin/env python

import argparse

#   Set and parse arguments
def set_args():
    """Set and parse the arguments here. There are three subroutines for this package:
        fix             Fix a pseudoscaffold file to be used by the annotator
        blast-config    Set the default arguments for BLAST to be used by the annotator
        annotate        Run the annotator itself"""
    #   Define the arguments
    Arguments = argparse.ArgumentParser(add_help=True)
    Sub_Args = Arguments.add_subparsers(help='')
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
        type=str,
        default='0.5',
        #action=
        metavar='EVALUE',
        help="Evalue for BLAST search, default is 0.5")
    Blast_Arguments.add_argument('-m',
        '--max_seqs',
        type=str,
        default='5',
        #action=
        metavar='MAX TARGET SEQUENCES',
        help="Maximum number of target sequences for BLAST search, default is 5")
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
    #   Parse the arguments
    args = Arguments.parse_args()
    return(args)
