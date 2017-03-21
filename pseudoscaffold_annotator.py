#!/usr/bin/env python3

"""potatoes"""

import sys
if sys.version_info.major is not 3 and sys.version_info.minor < 5:
    sys.exit("Please use Python 3.5 or higher for this program")

#   Import required modules from standard Python library
import os
import argparse
# import itertools
# from multiprocessing import Pool

#   Import functions defined in another script bundled with this package
# import Pseudoscaffold_Utilities.pseudoscaffold_tools as pseudoscaffold_tools
# import Miscellaneous_Utilities.argument_utilities as argument_utilities
# import Miscellaneous_Utilities.annotation_utilities as annotation_utilities
# import Miscellaneous_Utilities.blast_utilities as blast_utilities


# @typechecked
def _set_args() -> argparse.ArgumentParser:
    default_output = os.getcwd() + '/annotation'
    parser = argparse.ArgumentParser(
        add_help=True,
        formatter_class=argparse.RawTextHelpFormatter,
        prog=sys.argv[0],
        description='Foobar'
    )
    ref_opts = parser.add_argument_group(
        title='Reference Genomes',
        description="Provide a BLAST nucleotide database for the destination reference genome and a FASTA file for the source reference genome"
    )
    ref_opts.add_argument(
        '-d',
        '--destination-database',
        dest='destination',
        type=str,
        default=None,
        required=True,
        metavar='DESTINATION DATABASE',
        help="Destination reference genome in a BLAST nucleotide database"
    )
    ref_opts.add_argument(
        '-s',
        '--source-genome',
        dest='source',
        type=str,
        default=None,
        required=True,
        metavar='SOURCE REFERENCE GENOME',
        help="Source reference genome in FASTA format"
    )
    ann_opts = parser.add_argument_group(
        title='Source Annotation File',
        description="Provide an annotation file for the source reference genome in BED, GFF, or SAMTools Regions format"
    )
    ann_opts.add_argument(
        '-a',
        '--annotation',
        dest='annotation',
        type=str,
        default=None,
        required=True,
        metavar='SOURCE REFERENCE ANNOTATION',
        help="Annotation file for source reference genome"
    )
    out_opts = parser.add_argument_group(
        title='Output Options',
        description="Choose what files we output"
    )
    out_opts.add_argument(
        '-o',
        '--output-annotation',
        dest='output',
        type=str,
        default=default_output,
        required=False,
        metavar='OUTPUT ANNOTATION',
        help="Choose where we write the lifted annotations and what format we write them in. Defaults to " + default_output + " in the format provided by the source annotation file"
    )
    out_opts.add_argument(
        '-k',
        '--keep-xml',
        dest='keep_xml',
        action='store_const',
        const=True,
        default=False,
        required=False,
        help="Do we keep the XML results? Pas '-k | --keep-xml' to say yes"
    )
    return parser



#   Annotate the pseudoscaffold
#       Method dependent on the input and output annotation files
def pseudoscaffold_annotator(args, temppath, shellpath, pseudopath):
    """Start annotating the pseudoscaffold"""
#     #   Import the parallelized wrapper
#     import Pseudoscaffold_Utilities.wrapper as wrapper
#     #   Change to temp directory
#     if not os.getcwd() == temppath:
#         os.chdir(temppath)
#     #   Create full sequence list
#     seq_list = annotation_utilities.extraction_sh(args['reference'], args['annotation'], shellpath)
#     # #   Read the annotation, reference, and pseudoscaffold files
#     # annotation, reference, pseudoscaffold = annotation_utilities.opener(args['annotation'], args['reference'], args['pseudoscaffold'])
#     # #   Figure out what reference annotation file we have
#     # find_gff, find_bed = annotation_utilities.extension_searcher(gff, bed, args['annotation'])
#     # #   Figure out what pseudoscaffold annotation file we are making
#     # create_gff, create_bed = annotation_utilities.extension_creator(gff, bed, args['outfile'])
#     #   Read the BLAST config file
#     bconf = blast_utilities.blast_config_parser(args['cfile'])
#     #   Make the BLAST databae
#     database_name, out, err = blast_utilities.make_blast_database(bconf, shellpath, args['pseudoscaffold'], pseudopath, temppath)
#     #   Find the original contigs from the reference annotation
#     contig_original, length_final = pseudoscaffold_tools.contig_extracter(args['annotation'])
#     #   Set up a list of arguments
#     # ann_args = itertools.izip(itertools.repeat(seq_list), contig_original, itertools.repeat(args['annotation']), itertools.repeat(args['pseudoscaffold']), itertools.repeat(args['reference']), itertools.repeat(temppath), itertools.repeat(bconf), itertools.repeat(database_name), itertools.repeat(pseudopath), itertools.repeat(find_gff), itertools.repeat(find_bed), itertools.repeat(create_gff), itertools.repeat(create_bed))
#     # ann_args = itertools.izip(itertools.repeat(seq_list), contig_original, itertools.repeat(args['annotation']), itertools.repeat(args['pseudoscaffold']), itertools.repeat(args['reference']), itertools.repeat(temppath), itertools.repeat(bconf), itertools.repeat(database_name), itertools.repeat(pseudopath), itertools.repeat(args['outfile']))
#     ann_args = zip(zip(itertools.repeat(seq_list), contig_original, itertools.repeat(args['annotation']), itertools.repeat(args['pseudoscaffold']), itertools.repeat(args['reference']), itertools.repeat(temppath), itertools.repeat(bconf), itertools.repeat(database_name), itertools.repeat(pseudopath), itertools.repeat(args['outfile'])))
#     #   Annotate the pseudoscaffold in parallel
#     if __name__ == '__main__':
#         pool = Pool(processes=args['procs'])
#         pool.map(wrapper.args_wrapper, ann_args)
    pass


#   Do the work here
def main(args: dict) -> None:
    """Read arguments, determine which subroutine to run, and run it"""
    #   No arguments give, display usage message
    # parser = _set_args()
    # if not sys.argv[1:]:
    #     # argument_utilities.Usage()
    #     sys.exit(1)
    #   Create a dictionary of arguments
    # args = vars(argument_utilities.set_args())
    #   Run the 'fix' subroutine
    if args['command'] == 'fix':
        import Pseudoscaffold_Utilities.pseudoscaffold_fixer as pseudoscaffold_fixer
        pseudoscaffold_fixer.main(args['pseudoscaffold'], args['new_pseudoscaffold'])
        sys.exit(0)
    #   Run the 'blast-config' subroutine
    elif args['command'] == 'blast-config':
        # blast_utilities.make_blast_config(args)
        sys.exit(0)
    #   Run the 'annotate' subroutine
    elif args['command'] == 'annotate':
        # rootpath, tempdir, temppath, shellpath, pseudopath = annotation_utilities.tempdir_creator(args['pseudoscaffold'])
        # pseudoscaffold_annotator(args, temppath, shellpath, pseudopath)
        #annotation_utilities.annotation_builder(rootpath, tempdir, temppath, args['outfile'])
        pass
    #   Run the 'subset' subroutine
    elif args['command'] == 'subset':
        pass
        # import Miscellaneous_Utilities.subset_annotation as subset_annotation
        # subset_annotation.subset_annotation(args, gff, bed)
    #   Incorrect subroutine specified, display usage message
    else:
        # argument_utilities.Usage()
        sys.exit(1)

# main()

if __name__ == '__main__':
    PARSER = _set_args()
    if not sys.argv[1:]:
        sys.exit(PARSER.print_help())
    ARGS = vars(PARSER.parse_args())
    main(ARGS)
