#!/usr/bin/env python

#   A script to hold functions for finding fields in a GFF file

#       Find the seqid (column 1) from the GFF file
def contig_extracter(reference, annotation):
    contig = re.compile(ur'(^[a-zA-Z0-9_]+)', re.MULTILINE)
    contig_original = list()
    extracted_contig = contig.findall(annotation)
    length_checker = len(extracted_contig)
    for entry in extracted_contig:
        if not entry in contig_original:
            contig_original.append(entry)
        else:
            pass
    print("Original contigs found")
    return(contig_original, length_checker)


#       Find the source (column 2) from the GFF file
def source_finder(contig_original, annotation, length_checker):
    sources = list()
    for unique in contig_original:
        source_searcher = re.compile(ur'(?<=%s)\s+([a-zA-Z0-9]*)'%(unique))
        sourcer = source_searcher.findall(annotation)
        sources = sources + sourcer
    if len(sources) == length_checker:
        print("All 'source' fields found")
        return(sources)
    else:
        sys.exit("Failed to collect all 'source' fields from original annotation file")


#       Find the type (column 3) from the GFF file
def type_finder(contig_original, annotation, length_checker):
    types = list()
    for unique in contig_original:
        type_searcher = re.compile(ur'(?<=%s)\s+[a-zA-Z0-9]+\s+([a-zA-Z0-9_]*)'%(unique))
        typer = type_searcher.findall(annotation)
        types = types + typer
    if len(types) == length_checker:
        print("All 'type' fields found")
        return(types)
    else:
        sys.exit("Failed to collect all 'type' fields from original annotation file")


#       Find the score (column 6) from the GFF file
def score_finder(contig_original, annotation, length_checker):
    scores = list()
    for unique in contig_original:
        score_searcher = re.compile(ur'(?<=%s)\s+[a-zA-Z0-9]+\s+[a-zA-Z0-9_]+\s+[0-9]+\s+[0-9]+\s+([a-zA-Z0-9\._\-])'%(unique))
        scorer = score_searcher.findall(annotation)
        scores = scores + scorer
    if len(scores) == length_checker:
        print("All 'score' fields found'")
        return(scores)
    else:
        sys.exit("Failed to collect all 'score' fields from original annotation file")


#       Find the strand information (column 7) from the GFF file
def strandedness(contig_original, annotation, length_checker):
    strands = list()
    for unique in contig_original:
        strand_searcher = re.compile(ur'(?<=%s)\s+[a-zA-Z0-9]+\s+[a-zA-Z0-9_]+\s+[0-9]+\s+[0-9]+\s+[a-zA-Z0-9\._\-]\s+([+\-\.])'%(unique))
        strander = strand_searcher.findall(annotation)
        strands = strands + strander
    if len(strands) == length_checker:
        print("All 'strand' information found")
        return(strands)
    else:
        sys.exit("Failed to collect all 'strand' information from original annotation file")


#       Find the phase (column 8) from the GFF file
def phase_finder(contig_original, annotation, length_checker):
    phases = list()
    for unique in contig_original:
        phase_searcher = re.compile(ur'(?<=%s)\s+[a-zA-Z0-9]+\s+[a-zA-Z0-9_]+\s+[0-9]+\s+[0-9]+\s+[a-zA-Z0-9\._\-]\s+[+\-\.]\s+([\.012])'%(unique))
        phaser = phase_searcher.findall(annotation)
        phases = phases + phaser
    if len(phases) == length_checker:
        print("All 'phase' information found")
        return(phases)
    else:
        sys.exit("Failed to collect all 'phase' information from original annotation file")


#       Find any attributes (column 9) from the GFF file
def attribute_finder(contig_original, annotation, length_checker):
    attributes = list()
    for unique in contig_original:
        attribute_searcher = re.compile(ur'(?<=%s)\s+[a-zA-Z0-9]+\s+[a-zA-Z0-9_]+\s+[0-9]+\s+[0-9]+\s+[a-zA-Z0-9\._\-]\s+[+\-\.]\s+[\.012]\s+(.*)'%(unique))
        attributer = attribute_searcher.findall(annotation)
        attributes = attributes + attributer
    if len(attributes) == length_checker:
        print("All attributes found")
        return(attributes)
    else:
        sys.exit("Failed to collect all attributes from original annotation file")
