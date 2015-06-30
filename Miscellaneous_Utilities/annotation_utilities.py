#!/usr/bin/env python

"""A script to assemble the annotation piecies for the pseudoscaffold"""

#   Import required modules from standard Python library
import sys
import os
import re

def tempdir_creator():
    rootpath = os.getcwd()
    tempdir = 'temp'
    if re.search(tempdir, str(os.listdir('.'))):
        os.chdir(tempdir)
        temppath = os.getcwd()
    else:
        os.mkdir(tempdir)
        os.chdir(tempdir)
        temppath = os.getcwd()
    return(rootpath, tempdir, temppath)


#   Build the full annotaiton from its parts
def annotation_builder(rootpath, tempdir, temppath, outfile):
    if not os.getcwd() == temppath:
        os.chdir(temppath)
    file_list = str(os.listdir('.'))
    extension = outfile.split('.')[-1]
    file_finder = re.compile(ur'([a-zA-Z0-9-_\.]*)%s'%(extension))
    annotation_parts = file_finder.findall(file_list)
    annotation = open(outfile, 'a')
    for part in annotation_parts:
        part_data = open(part).read
        annotation.write(part_data)
    annotation.close()


#   Find the extension of the given annotation file
def extension_searcher(gff, bed, annotation):
    """Figure out the type (BED or GFF) of annotation file we're working with"""
    find_gff = gff.search(annotation)
    find_bed = bed.search(annotation)
    return(find_gff, find_bed)


#   Find the desired extension of the pseudoscaffold annotation file
def extension_creator(gff, bed, outfile):
    """Figure out the desired type (BED or GFF) of annotation file"""
    create_gff = gff.search(outfile)
    create_bed = bed.search(outfile)
    return(create_gff, create_bed)
