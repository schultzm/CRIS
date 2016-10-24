#!/usr/bin/env python

'''
Search for CRISPR binding sites in an annotated genbank sequence.
'''

import argparse
from Bio import SeqIO
from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord
from Bio.Alphabet import generic_dna
import re
from collections import defaultdict


#set up the arguments parser to deal with the command line input
PARSER = argparse.ArgumentParser(description='Find CRISPR binding sites.')
PARSER.add_argument('-s', '--seq_infile', help='DNA seq to scan.',
                    required=True)
# PARSER.add_argument('-p', '--PAM_seq', help='5\'to 3\' sequence at the\
#                      3\' end of the genomic target', default='NGG', required=False)
# PARSER.add_argument('-t', '--length_target', help='Length of genomic target.',
#                     required=False)

ARGS = PARSER.parse_args()

#The CRISPR binding site rule
SEQS = '[ATGC]{22}GG'



def readseq(seqinfile, seqinformat):
    '''
    Read in the sequence from file.  Return it as the variable 'sequence'.
    '''
    sequence = SeqIO.parse(seqinfile, seqinformat)
    return sequence

def gene_details(sequence):
    '''
    From the sequence, extract gene names and coordinates.
    '''
    pass

def main():
    '''
    Get sequence, extract genes and coordinates.
    '''
    seqn = readseq(ARGS.seq_infile, 'genbank')
    for gb_record in seqn:
        whole_gb_record_seq = gb_record.seq
        whole_gb_record_seq_rev = gb_record.seq.reverse_complement()
        for index, feature in enumerate(gb_record.features):
            if feature.type == 'gene':
                #Capture the whole feature in gb_feature.
                gb_feature = gb_record.features[index]
                #Store a name for the feature if it is a gene
                if 'gene' in feature.qualifiers:
                    locus_name = feature.qualifiers['gene'][0]
                else:
                    locus_name = feature.qualifiers['locus_tag'][0]
                print '\n', locus_name
                #Store the location of the locus
                locus_location = feature.location
                locus_start = locus_location.start
                locus_end = locus_location.end
                locus_strand = locus_location.strand
                print locus_location, locus_strand
                #Store the DNA sequence of the feature
                gene_seq = gb_feature.extract(gb_record.seq).upper()
                gene_seq_rev = gb_feature.extract(gb_record.seq).upper().reverse_complement()
                #Find the possible CRISPR sites in the gene, stored as a list
                #SEQS is a regular expression to define the CRISPR rule
                potential_CRISPR_seqs = re.findall(SEQS, str(gene_seq))
                finalists = []
                #Check if they hit elsewhere in the whole_gb_record_seq or its revcomp
                for potential_CRISPR_seq in potential_CRISPR_seqs:
                    #Find the location of the potential_CRISPR_seq (list)
                    #Search forward and reverse
                    whole_gb_record_CRISPR_locs = re.finditer(potential_CRISPR_seq, str(whole_gb_record_seq))
                    whole_gb_record_rev_CRISPR_locs = re.finditer(potential_CRISPR_seq, str(whole_gb_record_seq_rev))
#                     print list(whole_gb_record_CRISPR_locs)
#                     whole_gb_record_CRISPR_locs
#                     print whole_gb_record_CRISPR_locs
                    locs_forward = [(i.start(), i.end()) for i in whole_gb_record_CRISPR_locs]
                    locs_reverse = [(i.start(), i.end()) for i in whole_gb_record_rev_CRISPR_locs]
                    if len(locs_forward) + len(locs_reverse) != 1:
                        # get out of loop if there is more than one match
                        print 'No potential CRISPR sites found.'
                        break
#                     if len(locs_forward) == 1:
#                         
#                         if len(locs_forward) == 0 and locus_strand < 0 and len(locs_reverse) == 1:
#                             loc_start = locs_reverse[0][0]
#                             loc_end = locs_reverse[0][1]
                    
                    
#                     if len(locs_forward) == 1 and locus_strand > 0 and locus_start<=locs_forward[0][0]<locus_end and locus_start<=locs_forward[0][1]<locus_end:
#                         print potential_CRISPR_seq, locs_forward
#                     if len(locs_reverse) == 1 and locus_strand < 0:
#                         print potential_CRISPR_seq, locs_reverse
#                     print locs_forward, locs_reverse
#                     for whole_gb_record_CRISPR_loc in whole_gb_record_CRISPR_locs:
#                         strt = whole_gb_record_CRISPR_loc.start()
#                         stp = whole_gb_record_CRISPR_loc.end()
#                         print locus_start
#                         if strt >= locus_start and stp <= locus_end:
#                             print potential_CRISPR_seq, strt, stp
#                     print ''
#                         print whole_gb_record_CRISPR_loc.start()+locus_start
#                         recrd = SeqRecord(Seq(site, alphabet=generic_dna), name = locus_name+'_'+site, description='CRISPR site', id=site, location=[1:1])
#                         print recrd
#                         CRISPR_site_location = (potential_CRISPR_loc.start(), potential_CRISPR_loc.end())
#                         whole_gb_forward_CRISPR_hits = re.findall(potential_CRISPR_seq, str(whole_gb_record_seq))
#                         whole_gb_forward_CRISPR_hits_pos = re.finditer(potential_CRISPR_seq, str(whole_gb_record_seq))
#                         for loc in whole_gb_forward_CRISPR_hits_pos:
#                             print whole_gb_forward_CRISPR_hits, loc.start(), loc.end()
#                             print site_locs
#                         print 'forward', whole_genome_hits
#                         whole_genome_hits_rev = re.findall(site, str(whole_seq_rev))
#                         print 'reverse', whole_genome_hits_rev
#                         print site_locs

if __name__ == '__main__':
    main()
    
    
