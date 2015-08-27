#!/usr/bin/env python

#   Import required modules from standard Python library
import os
import sys
import re

#   Import functions defined in another script bundled with this package
import Pseudoscaffold_Utilities.pseudoscaffold_tools as pseudoscaffold_tools
import Miscellaneous_Utilities.argument_utilities as argument_utilities
import Miscellaneous_Utilities.annotation_utilities as annotation_utilities
import Miscellaneous_Utilities.blast_utilities as blast_utilities

#   Create two regex objects for determining given and desired file extensions
gff = re.compile(ur'(.*\.gff$)')
bed = re.compile(ur'(.*\.bed$)')


#   Annotate the pseudoscaffold
#       Method dependent on the input and output annotation files
def pseudoscaffold_annotator(args, temppath, rootpath, shellpath, pseudopath):
    """Start annotating the pseudoscaffold"""
    #   Import the parallelized wrapper
    import Miscellaneous_Utilities.wrapper as wrapper
    #   Change to temp directory
    if not os.getcwd() == temppath:
        os.chdir(temppath)
    #   Create full sequence list
    seq_list = annotation_utilities.extraction_sh(args['reference'], args['annotation'], shellpath)
    #   Read the annotation, reference, and pseudoscaffold files
    annotation, reference, pseudoscaffold = annotation_utilities.opener(args['annotation'], args['reference'], args['pseudoscaffold'])
    #   Figure out what reference annotation file we have
    find_gff, find_bed = annotation_utilities.extension_searcher(gff, bed, args['annotation'])
    #   Figure out what pseudoscaffold annotation file we are making
    create_gff, create_bed = annotation_utilities.extension_creator(gff, bed, args['outfile'])
    #   Read the BLAST config file
    bconf = blast_utilities.blast_config_parser(args['cfile'])
    #   Make the BLAST databae
    database_name, out, err = blast_utilities.make_blast_database(bconf, shellpath, args['pseudoscaffold'], pseudopath, temppath)
    #   Find the original contigs from the reference annotation
    contig_original, length_final = pseudoscaffold_tools.contig_extracter(annotation)
    #   Set up a list of arguments
    ann_args = itertools.izip(itertools.repeat(seq_list), contig_original, itertools.repeat(annotation), itertools.repeat(pseudoscaffold), out, itertools.repeat(temppath), itertools.repeat(bconf), itertools.repeat(database_name), itertools.repeat(pseudopath), itertools.repeat(find_gff), itertools.repeat(find_bed), itertools.repeat(create_gff), itertools.repeat(create_bed))
    #   Annotate the pseudoscaffold in parallel
        if __name__ == '__main__':
            pool = Pool(processes=args['procs'])
            pool.map( wrapper.args_wrapper, ann_args)


#   Do the work here
def main():
    """Read arguments, determine which subroutine to run, and run it"""
    #   No arguments give, display usage message
    if not sys.argv[1:]:
        argument_utilities.Usage()
        sys.exit(1)
    #   Create a dictionary of arguments
    args = vars(argument_utilities.set_args())
    #   Run the 'fix' subroutine
    if args['command'] == 'fix':
        import Pseudoscaffold_Utilities.pseudoscaffold_fixer as pseudoscaffold_fixer
        pseudoscaffold_fixer.main(args['pseudoscaffold'], args['new_pseudoscaffold'])
        sys.exit(0)
    #   Run the 'blast-config' subroutine
    elif args['command'] == 'blast-config':
        blast_utilities.make_blast_config(args)
        sys.exit(0)
    #   Run the 'annotate' subroutine
    elif args['command'] == 'annotate':
        rootpath, tempdir, temppath, shellpath, pseudopath = annotation_utilities.tempdir_creator(args['pseudoscaffold'])
        pseudoscaffold_annotator(args, temppath, rootpath, shellpath, pseudopath)
        #annotation_utilities.annotation_builder(rootpath, tempdir, temppath, args['outfile'])
    #   Run the 'subset' subroutine
    elif args['command'] == 'subset':
        import Miscellaneous_Utilities.subset_annotation as subset_annotation
        subset_annotation.subset_annotation(args, gff, bed)
    #   Incorrect subroutine specified, display usage message
    else:
        argument_utilities.Usage()
        sys.exit(1)

main()
