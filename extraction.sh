#!/bin/bash

FASTA=$1
BED=$2
OUT=$3

bedtools getfasta -fi $FASTA -bed $BED -fo $OUT