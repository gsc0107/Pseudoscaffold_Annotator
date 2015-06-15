#!/usr/bin/env python

import sys

def opener(pseudoscaffold, outfile):
    pseudo = open(pseudoscaffold).read()
    fixed = open(outfile, 'w')
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


def main(pseuodoscaffold, outfile):
    pseudo, fixed = opener(pseuodoscaffold, outfile)
    pseudo_indecies = contig_extracter(pseudo)
    pseudoscaffold_fixer(pseudo, pseudo_indecies, fixed)
