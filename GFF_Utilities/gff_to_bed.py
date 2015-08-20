#!/usr/bin/env python

"""A script to create a BED annotation from a reference GFF file"""

#   Import required modules from standard Python library
import re
import os

#   Import functions defined in custom modules
import Pseudoscaffold_Utilities.pseudoscaffold_tools as pseudoscaffold_tools
import Miscellaneous_Utilities.blast_utilities as blast_utilities
import GFF_Utilities.gff_extracter as gff_extracter


#   A class to handle making the BED annotation
class gffBED(object):
    def __init__(self, seq_list, unique, reference, annotation, pseudoscaffold, outfile, temppath, bconf, database_name, pseudopath):
        self.seq_list = seq_list
        self.unique = unique
        self.reference = reference
        self.annotation = annotation
        self.pseudoscaffold = pseudoscaffold
        self.outfile = outfile
        self.temppath = temppath
        self.bconf = bconf
        self.database_name = database_name
        self.pseudopath = pseudopath
        return


    #   Find the number of times this contig shows up in original annotation file
    def find_length(self):
        """Creates a check for each part of the extraction process to ensure the correct amount of data is gathered from the original annotation file.
            The unique argument is the contig to search for within the annotation file.
            The annotation argument is the original annotation file"""
        contig = re.compile(ur'(%s)\t'%(self.unique))
        length = contig.findall(self.annotation)
        length_checker = len(length)
        print("There should be " + str(length_checker) + " sequences")
        return(length_checker)


    #   Make a BED3 file
    def bed3_builder(self, titles, starts, ends, length_checker):
        """Builds a BED3 filed from extracted components of original GFF file"""
        bed3=open(self.outfile, 'w')
        print("Opened " + self.outfile + " for writing")
        for i in range(0, length_checker):
            bed3.write(str(titles[i]))
            bed3.write('\t')
            bed3.write(str(starts[i]))
            bed3.write('\t')
            bed3.write(str(ends[i]))
            bed3.write('\n')
        bed3.close()
        print("BED file created")
        return


    #   Do the work here
    def gff_to_bed(self):
        """Extract information from original annotation file and match it up to sequences defined in pseudoscaffold. Then build a BED annotation using this data for the pseudoscaffold"""
        print("Working on finding " + self.unique + " in the pseudoscaffold")
        if not os.getcwd() == self.temppath:
            os.chdir(self.temppath)
        length_checker = self.find_length()
        unique_sequences = pseudoscaffold_tools.sequence_finder(self.seq_list, self.unique)
        itles, starts, ends = blast_utilities.run_blast(self.bconf, unique_sequences, self.database_name, length_checker, self.temppath, self.pseudopath, self.unique, types)
        self.bed3_builder(titles, starts, ends, length_checker)
        return
