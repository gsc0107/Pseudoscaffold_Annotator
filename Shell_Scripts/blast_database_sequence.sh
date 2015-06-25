#!/bin/bash

#   A small shell script to retrieve sequences
#   from a local BLAST search

set -e
set -u
set -o pipefail

#   Test to make sure NCBI's BLAST+ is installed
#   specifically `blastdbcmd`

if `command -v blastdbcmd > /dev/null 2> /dev/null`
then
    echo "BLAST+ installed"
else
    echo "You need NCBI's BLAST+ utilities installed and in your path"
    exit 1
fi

#   our arguments
DATABASE=
DATABASE_TYPE
OUTFILE=
OUT_FORMAT="%f"
INPUT_

blastdbcmd -entry ? -db $DATABASE -dbtype = $DATABASE_TYPE -out $OUTFILE -outfmt $OUT_FORMAT
