#!/bin/bash

#   A small shell script to make a BLAST database
#   out of an input pseudoscaffold

set -e
set -u
set -o pipefail

#   Test to make sure NCBI's BLAST+ is installed
#   specifically `makeblastdb`

if `command -v makeblastdb > /dev/null 2> /dev/null`
then
    echo "BLAST+ installed" >&2
else
    echo "You need NCBI's BLAST+ utilities installed and in your PATH" >&2
    exit 1
fi

echo "$@" >> args.txt
echo "$#" >> args.txt

exit 0

#INPUT_PSEUDOSCAFFOLD="$1"
#OUTPUT_DATABASE="$2"
#DB_TYPE="$3"
#EXT="$4"

#makeblastdb -in ${INPUT_PSEUDOSCAFFOLD} -dbytpe ${DB_TYPE} -out ${OUTPUT_DATABASE}
