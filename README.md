# pseudoscaffold_annotator
### A program to annotate an assembled pseudoscaffold
___
___

This is a program for annotating an assembled pseudoscaffold using a reference genome and annotation file. Currently, this only supports using GFF3 files as input, but can output both GFF3 files and 3-column BED files. Increased support for the BED format will come later.

Running this program to annotate a pseudoscaffold is done using the following command:

```shell
./pseudoscaffold_annotator.py annotate -r REFERENCE_FASTA -a ORIGINAL_ANNOTATION -p PSEUDOSCAFFOLD_FASTA -o OUTFILE_NAME -c BLAST_CONFIG_FILE
```

The BLAST configuration file can be run using the following command:

```shell
./pseudoscaffold_annotator.py blast-config
```
Use the `-h` flag to see all options for configuring.

**IMPORTANT**

pseudoscaffold_annotator.py requires no new lines within the sequence of the pseudoscaffold. The following is not an allowed sequence:

        >pseudoscaffold
        ACTGTCAG
        GCTATCGA

The 'fix' subroutine removes new lines
between sequence data, creating a fasta
file that reads like:
        >pseudoscaffold
        ACTGTCAGGCTATCGA

To fix a pseudoscaffold, run the following command:

```shell
./pseudoscaffold_annotator.py fix -p PSEUDOSCAFFOLD_FASTA -n FIXED_FASTA
```

This program requires Python 2.7 or higher, or the [`argparse`](https://pypi.python.org/pypi/argparse) module installed for Python 2.6

**NOTE: this has NOT been tested on Python 3.x**

Other dependencies include:
 - [BEDTools](http://bedtools.readthedocs.org/en/latest/)
 - [NCBI's BLAST+](http://blast.ncbi.nlm.nih.gov/Blast.cgi?PAGE_TYPE=BlastDocs&DOC_TYPE=Download)
 - [BioPython](http://biopython.org/wiki/Main_Page)

**NOTE: This program has only been tested with the _Morex_ (Barley) genome, please use with caution**

## TODO

 - Add support for extracting information from BED file
 - Add parallelization support
 - Add BED to GFF annotating capabilities
 - Add GFF to BED annotating capabilities
 - ~~Finish GFF to GFF annotation capabilities~~ DONE!
 - Add BED to BED annotating capabilities
