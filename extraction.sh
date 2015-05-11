#!/bin/bash

set -e
set -u
set -o pipefail

FASTA=$1
BED=$2
OUT=$3

bedtools getfasta -fi $FASTA -bed $BED -fo $OUT
