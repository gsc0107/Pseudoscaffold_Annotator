#!/usr/bin/env python

"""A script to fix the formatting in a pseudoscaffold so that it can be annotated by the main program by getting rid of any new lines within sequence data"""

#   Import required modules from standard Python library
import sys
import re

#   Open the pseudoscaffold for reading and the outfile for writing
def opener(pseudoscaffold, outfile):
    """Opens the original pseudoscaffold for reading and the outfile for writing the new pseudoscaffold"""
    pseudo = open(pseudoscaffold).read()
    fixed = open(outfile, 'w')
    return(pseudo, fixed)


#   Get a list of all
def contig_extracter(pseudo, num):
    """Finds the pseudoscaffold IDs. These IDs must contain numbers, lowercase letters, or underscores only."""
    scaffolds = re.compile(ur'(>[0-9a-z\_]+)')
    pseudo_indecies = scaffolds.findall(pseudo)
    return(pseudo_indecies)


#   Perform the fixing
def pseudoscaffold_fixer(pseudo, pseudo_indecies, fixed):
    """Split and reassemble the pseudoscaffold piece by piece. This function splits the original pseudoscaffold up by new line and reassembles it into a new pseudoscaffold file formatted so that it can be used by the annotation scripts"""
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

#   Do the work
def main(pseuodoscaffold, outfile):
    """Utilize the other functions within this module to fix the pseudoscaffold file"""
    pseudo, fixed = opener(pseuodoscaffold, outfile)
    pseudo_indecies = contig_extracter(pseudo)
    pseudoscaffold_fixer(pseudo, pseudo_indecies, fixed)
