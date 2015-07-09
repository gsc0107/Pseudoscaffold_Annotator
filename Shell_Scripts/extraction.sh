#!/bin/bash

set -e
set -u
set -o pipefail

#   Check to see if BEDTools is installed
if `command -v bedtools > /dev/null 2> /dev/null`
then
    echo "BEDTools is installed"
else
    echo "Please install BEDTools and put in your path"
    exit 1
fi

FASTA=$1
BED=$2
OUT=$3

bedtools getfasta -fi $FASTA -bed $BED -fo $OUT
