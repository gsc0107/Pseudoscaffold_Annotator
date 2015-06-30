#!/usr/bin/env python

#   Import required modules from standard Python library
import subprocess
import os
import sys
import re

#   Import functions from the multiprocessing module
from multiprocessing import Process, Lock

#   Import functions defined in another script bundled with this package
import Pseudoscaffold_Tools.pseudoscaffold_tools as pseudoscaffold_tools
import Miscellaneous_Utilities.argument_utilities as argument_utilities

#   Create two regex objects for determining given and desired file extensions
gff = re.compile(ur'(.*\.gff$)')
bed = re.compile(ur'(.*\.bed$)')


#   Open the files
def opener(annotation, reference, pseudoscaffold):
    """Open the reference annotation, reference sequence, and pseudoscaffold for working"""
    annotations = open(annotation).read()
    references = open(reference).read()
    pseudoscaffolds = open(pseudoscaffold).read()
    print("Opened all files")
    return(annotations, references, pseudoscaffolds)


#   Create a FASTA file of sequences defined by original annotation file
def extraction_sh(reference, annotation, rootpath):
    """Extract the sequences defined by the annotation file from the refernce fasta file"""
    tmp = 'pseudoscaffold_annotator_temp.fasta'
    print("Searching for original sequences using 'extraction.sh'")
    extraction_script = str(rootpath + '/Shell_Scripts/extraction.sh')
    extraction_cmd = ['bash', extraction_script, reference, annotation, tmp]
    extraction_shell = subprocess.Popen(extraction_cmd, shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = extraction_shell.communicate()
    seq_list = open(tmp).read()
    os.remove(tmp)
    return(seq_list)


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

#   Annotate the pseudoscaffold
#       Method dependent on the input and output annotation files
def pseudoscaffold_annotator(args, temppath, rootpath):
    """Start annotating the pseudoscaffold"""
    if not os.getcwd() == temppath:
        os.chdir(temppath)
    seq_list = extraction_sh(args['reference'], args['annotation'], rootpath)
    annotation, reference, pseudoscaffold = opener(args['annotation'], args['reference'], args['pseudoscaffold'])
    find_gff, find_bed = extension_searcher(gff, bed, args['annotation'])
    create_gff, create_bed = extension_creator(gff, bed, args['outfile'])
    if find_gff and create_gff:
        print "Found GFF file, making GFF file"
        import GFF_Tools.gff_to_gff as gff_to_gff
        import GFF_Tools.gff_extracter as gff_extracter
        contig_original, length_final = gff_extracter.contig_extracter(annotation)
        if __name__ == '__main__':
            lock = Lock()
            for unique in contig_original:
                out=str(unique+"_out.gff")
                print out
                Process(target=gff_to_gff.gff_to_gff, args=(lock, seq_list, unique, reference, annotation, pseudoscaffold, out, temppath)).start()
    elif find_gff and create_bed:
        print "Found GFF file, making BED file"
        import GFF_Tools.gff_to_bed as gff_to_bed
        import GFF_Tools.gff_extracter as gff_extracter
        contig_original, length_checker = gff_extracter.contig_extracter(reference, annotation)
        if __name__ == '__main__':
            lock = Lock()
            for unique in contig_original:
                out = str(unique+"_out.bed")
                pass
        pass
    elif find_bed and create_gff:
        print "Found BED file, making GFF file"
        import BED_Tools.bed_to_gff as bed_to_gff
        pass
    elif find_bed and create_bed:
        print "Found BED file, making BEd file"
        import BED_Tools.bed_to_bed as bed_to_bed
        pass
    else:
        sys.exit("Could not determine neither file format of input nor desired format of output file. Please make sure extensions are typed out fully.")

#   Do the work here
def main():
    """Read arguments, determine which subroutine to run, and run it"""
    if not sys.argv[1:]:
        argument_utilities.Usage()
        exit(1)
    args = vars(argument_utilities.set_args())
    print(args)
    if args['command'] == 'fix':
        import Pseudoscaffold_Tools.pseudoscaffold_fixer as pseudoscaffold_fixer
        pseudoscaffold_fixer.main(args['pseudoscaffold'], args['pseudoscaffold_fixer'])
    elif args['command'] == 'blast-config':
        pass
    elif args['command'] == 'annotate':
        import Miscellaneous_Utilities.annotation_utilities as annotation_utilities
        rootpath, tempdir, temppath = annotation_utilities.tempdir_creator()
        pseudoscaffold_annotator(args, temppath, rootpath)
        annotation_utilities.annotation_builder(rootpath, tempdir, temppath, args['outfile'])
    else:
        argument_utilities.Usage()
        exit(1)

main()
