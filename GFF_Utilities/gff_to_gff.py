#!/usr/bin/env python

"""A script to build a GFF annotation with a reference GFF file"""

#   Import required modules from standard Python library
import re
import os

#   Import functions defined in another script bundled with this package
import Pseudoscaffold_Utilities.pseudoscaffold_tools as pseudoscaffold_tools
import Miscellaneous_Utilities.blast_utilities as blast_utilities
import gff_extracter


#   A class to handle making creating a GFF annotation while extracting information from a reference GFF annotation
class GFF(object):
    def __init__(self, seq_list, unique, reference, annotation, pseudoscaffold, outfile, temppath, bconf, database_name):
        self.seq_list = seq_list
        self.unique = unique
        self.reference = reference
        self.annotation = annotation
        self.pseudoscaffold = pseudoscaffold
        self.outfile = outfile
        self.temppath = temppath
        self.bconf = bconf
        self.database_name = database_name
        return

    #   Find the number of times this a contig shows up in original annotation file
    def find_length(self):
        """Creates a check for each part of the extraction process to ensure the correct amount of data is gathered from the original annotation file.
            The unique argument is the contig to search for within the annotation file.
            The annotation argument is the original annotation file"""
        contig = re.compile(ur'(%s)'%(self.unique))
        length = contig.findall(self.annotation)
        length_checker = len(length)
        print length_checker
        return(length_checker)

#   Build the GFF file
    def gff3_builder(self, titles, sources, types, starts, ends, scores, strands, phases, attributes, length_checker):
        """Builds a GFF file from extracted components of original GFF file"""
        gff= open(self.outfile, 'w')
        print("Opened " + outfile + " for writing")
        for i in range(0, length_checker):
            gff.write(str(titles[i]))
            gff.write('\t')
            gff.write(str(sources[i]))
            gff.write('\t')
            gff.write(str(types[i]))
            gff.write('\t')
            gff.write(str(starts[i]))
            gff.write('\t')
            gff.write(str(ends[i]))
            gff.write('\t')
            gff.write(str(scores[i]))
            gff.write('\t')
            gff.write(str(strands[i]))
            gff.write('\t')
            gff.write(str(phases[i]))
            gff.write('\t')
            gff.write(str(attributes[i]))
            gff.write('\n')
        gff.close()
        print("GFF file created")
        return

    #   Do the work here
    def gff_to_gff(self):
        """Extract information from original annotation file and match it up to sequences defined in pseudoscaffold. Then build a GFF annotation using this data for the pseudoscaffold"""
        #lock.acquire()
        print("Working on finding " + self.unique + " in the pseudoscaffold")
        if not os.getcwd() == self.temppath:
            os.chdir(self.temppath)
        length_checker = self.find_length(self.unique, self.annotation)
        sources = gff_extracter.source_finder(self.unique, self.annotation, length_checker)
        types = gff_extracter.type_finder(self.unique, self.annotation, length_checker)
        scores = gff_extracter.score_finder(self.unique, self.annotation, length_checker)
        strands = gff_extracter.strandedness(self.unique, self.annotation, length_checker)
        phases = gff_extracter.phase_finder(self.unique, self.annotation, length_checker)
        attributes = gff_extracter.attribute_finder(self.unique, self.annotation, length_checker)
        # extracted_sequence = pseudoscaffold_tools.sequence_extracter(self.seq_list, self.unique)
        # contig_pseudo = pseudoscaffold_tools.contig_finder(extracted_sequence, length_checker, pseudoscaffold)
        # start, end = pseudoscaffold_tools.length_gff(extracted_sequence, length_checker, self.pseudoscaffold)
        unique_sequences = pseudoscaffold_tools.sequence_finder(self.seq_list, self.unique)
        titles, starts, ends = blast_utilities.run_blast(self.bconf, unique_sequences, self.database_name, length_checker)
        self.gff3_builder(outfile, titles, sources, types, starts, ends, scores, strands, phases, attributes, length_checker)
        #lock.release()
        return
