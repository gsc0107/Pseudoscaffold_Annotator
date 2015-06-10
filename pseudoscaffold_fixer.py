#!/usr/bin/env python

import argparse
import sys

Arguments = argparse.ArgumentParser(add_help=True)
Arguments.add_argument('-p',
    '--pseudoscaffold',
    type=str,
    default=None,
    metavar='ORIGINAL PSEUDOSCAFFOLD',
    help="Original pseudoscaffold fasta file to be fixed")

Arguments.add_argument('-o',
    '--outfile',
    type=str,
    default='fixed_pseudoscaffold.fasta',
    metavar='FIXED PSEUDOSCAFFOLD',
    help="Desired name of fixed pseudoscaffold fasta file. Please put full file name, including extenstion. Default is 'fixed_pseudoscaffold.fasta'")

args = Arguments.parse_args()


def Usage():
    print'''Usage: pseudoscaffold_fixer.py -p | --pseudoscaffold <original pseudoscaffold fasta file> -o | --outfile <name of fixed pseudoscaffold fasta file>

pseudoscaffold_fixer.py assembles a new pseudoscaffold fasta
file for use with Pseudoscaffold_Annotator.py

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


def opener():
    pseudo = open(args.pseudoscaffold).read()
    fixed = open(args.outfile, 'w')
    return(pseudo, fixed)


def contig_extracter(pseudo):
    pseudo_indecies = list()
    for i in range(1, 26):
        pseudo_indecies.append(pseudo.index('>%s'%(i)))
    pseudo_indecies.sort()
    return(pseudo_indecies)


def pseudoscaffold_fixer(pseudo, pseudo_indecies, fixed):
    pseudo = pseudo.splitlines()
    try:
        for i in range(0, len(pseudo_indecies)):
            fixed.write(pseudo[pseudo_indecies[i]])
            fixed.write('\n')
            fixed.write("".join(pseudo[pseudo_indecies[i]+1:pseudo_indecies[i+1]-1]))
            fixed.write('\n')
    except IndexError:
        fixed.write("".join(pseudo[pseudo_indecies[len(pseudo_indecies)-1]+1:len(pseudo)-1]))
        fixed.write('\n')
    fixed.close()


def main():
    if not sys.argv[1:]:
        Usage()
        exit(1)
    else:
        pseudo, fixed = opener()
        pseudo_indecies = contig_extracter(pseudo)
        pseudoscaffold_fixer(pseudo, pseudo_indecies, fixed)

main()
