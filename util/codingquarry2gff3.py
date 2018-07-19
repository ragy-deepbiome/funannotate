#!/usr/bin/env python

import sys, os, argparse

#setup menu with argparse
class MyFormatter(argparse.ArgumentDefaultsHelpFormatter):
    def __init__(self, prog):
        super(MyFormatter, self).__init__(prog, max_help_position=48)
parser = argparse.ArgumentParser(prog='gff2prot.py', 
    description = '''Script to convert CodingQuarry GFF3 to proper GFF3 format.''',
    epilog = """Written by Jon Palmer (2018) nextgenusfs@gmail.com""",
    formatter_class = MyFormatter)
parser.add_argument('-i', '--input', required=True, help='CodingQuarry annotation file')
parser.add_argument('-n', '--numbering', default=1, type=int, help='Gene numbering starts at')
args=parser.parse_args()

sys.stdout.write(("##gff-version 3\n"))
exonCounts = {}
GeneCount = args.numbering
geneRef = {}
with open(args.input, 'rU') as infile:
	for line in infile:
		line = line.strip()
		contig, source, feature, start, end, score, strand, phase, attributes = line.split('\t')
		ID,Parent,Name = (None,)*3
		info = attributes.split(';')
		for x in info:
			if x.startswith('ID='):
				ID = x.replace('ID=', '')
			elif x.startswith('Parent='):
				Parent = x.replace('Parent=', '')
			elif x.startswith('Name='):
				Name = x.replace('Name=', '')
		if ID and ' ' in ID:
			ID = ID.split(' ')[0]
		if Parent and ' ' in Parent:
			Parent = Parent.split(' ')[0]
		if feature == 'gene':
			geneID = 'gene_'+str(GeneCount)
			transID = 'transcript_'+str(GeneCount)+'-T1'
			#if not ID in geneRef:
			#	geneRef[ID] = (geneID, transID)
			sys.stdout.write('{:}\t{:}\t{:}\t{:}\t{:}\t{:}\t{:}\t{:}\tID={:};Name={:};Alias={:};\n'.format(contig,source,feature, start, end, score, strand, phase, geneID, geneID, ID))
			sys.stdout.write('{:}\t{:}\t{:}\t{:}\t{:}\t{:}\t{:}\t{:}\tID={:};Parent={:};Alias={:};\n'.format(contig,source,'mRNA', start, end, '.', strand, '.',transID, geneID, ID))
			GeneCount += 1
		elif feature == 'CDS':
			trimID = ID.replace('CDS:', '')
			#if trimID in geneRef:
			#	geneID,transID = geneRef.get(trimID)
			if not transID in exonCounts:
				exonCounts[transID] = 1
			else:
				exonCounts[transID] += 1
			num = exonCounts.get(transID)
			sys.stdout.write('{:}\t{:}\t{:}\t{:}\t{:}\t{:}\t{:}\t{:}\tID={:}.exon{:};Parent={:};\n'.format(contig,source,'exon', start, end, '.', strand, '.',transID, num, transID))
			sys.stdout.write('{:}\t{:}\t{:}\t{:}\t{:}\t{:}\t{:}\t{:}\tID={:}.cds;Parent={:};\n'.format(contig,source,feature, start, end, score, strand, phase, transID, transID))
