#!/usr/bin/env python

"""A script to assemble the annotation piecies for the pseudoscaffold"""

#   Import required modules from standard Python library
import sys
import os
import re

def tempdir_creator():
    rootpath = os.getcwd()
    tempdir = 'temp'
    os.mkdir(tempdir)
    os.chdir(tempdir)
    temppath = os.getcwd()
    return(rootpath, tempdir, temppath)


#   Build the full annotaiton from its parts
def annotation_builder(rootpath, tempdir, temppath, outfile):
    if not os.getcwd() == temppath:
        os.chdir(temppath)
    file_list = os.listdir('.')
    extension = outfile.split('.')[-1]
    file_finder = re.compile(ur'([a-zA-Z0-9-_\.]*)%s'%(extension))
    annotation_parts = file_finder.findall(file_list)
    annotation = open(outfile, 'a')
    for part in annotation_parts:
        part_data = open(part).read
        annotation.write(part_data)
    annotation.close()