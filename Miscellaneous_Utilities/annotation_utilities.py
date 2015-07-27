#!/usr/bin/env python

"""A script to hold various functions for building an annotation file for the pseudoscaffold"""

#   Import required modules from standard Python library
import subprocess
import sys
import os
import re


#   Open the files
def opener(annotation, reference, pseudoscaffold):
    """Open the reference annotation, reference sequence, and pseudoscaffold for working"""
    annotations = open(annotation).read()
    references = open(reference).read()
    pseudoscaffolds = open(pseudoscaffold).read()
    print("Opened all files")
    return(annotations, references, pseudoscaffolds)


#   Create a temporary directory
def tempdir_creator(pseudoscaffold):
    """Create a temporary directory for partial annotation files, find the 'Shell_Scripts' directory, and find the path to the pseudoscaffold for making the blast database"""
    rootpath = os.getcwd()
    rootlist = str(os.listdir(rootpath))
    if re.search('Shell_Scripts', rootlist):
        shellpath = rootpath + '/Shell_Scripts'
    else:
        sys.exit("Cannot find 'Shell_Script' directory")
    tempdir = 'temp'
    if re.search(tempdir, rootlist):
        os.chdir(tempdir)
        temppath = os.getcwd()
    else:
        os.mkdir(tempdir)
        os.chdir(tempdir)
        temppath = os.getcwd()
    pseudopath = os.path.dirname(os.path.abspath(pseudoscaffold))
    return(rootpath, tempdir, temppath, shellpath, pseudopath)


#   Create a FASTA file of sequences defined by original annotation file
def extraction_sh(reference, annotation, shellpath):
    """Extract the sequences defined by the annotation file from the refernce fasta file"""
    tmp = 'pseudoscaffold_annotator_temp.fasta'
    print("Searching for original sequences using 'extraction.sh'")
    extraction_script = str(shellpath + '/extraction.sh')
    extraction_cmd = ['bash', extraction_script, reference, annotation, tmp]
    extraction_shell = subprocess.Popen(extraction_cmd, shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = extraction_shell.communicate()
    seq_list = open(tmp).read()
    os.remove(tmp)
    return(seq_list)


#   Build the full annotaiton from its parts
def annotation_builder(rootpath, tempdir, temppath, outfile):
    """Build the full annotation file from the partial annotaiton files"""
    if not os.getcwd() == temppath:
        os.chdir(temppath)
    file_list = str(os.listdir('.'))
    extension = outfile.split('.')[-1]
    file_finder = re.compile(ur'([a-zA-Z0-9-_\.]*)%s'%(extension))
    annotation_parts = file_finder.findall(file_list)
    annotation = open(rootpath + '/' + outfile, 'a')
    for part in annotation_parts:
        part_data = open(part).read
        annotation.write(part_data)
    annotation.close()


#   Find the extension of the given annotation file
def extension_searcher(gff, bed, annotation):
    """Figure out the type (BED or GFF) of annotation file we're working with"""
    print("Figuring out what kind of annotation file was given")
    find_gff = gff.search(annotation)
    find_bed = bed.search(annotation)
    return(find_gff, find_bed)


#   Find the desired extension of the pseudoscaffold annotation file
def extension_creator(gff, bed, outfile):
    """Figure out the desired type (BED or GFF) of annotation file"""
    print("Figuring out what kind of annotation file is desired")
    create_gff = gff.search(outfile)
    create_bed = bed.search(outfile)
    return(create_gff, create_bed)
