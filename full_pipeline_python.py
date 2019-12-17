#Zebra filter full pipeline

import pandas as pd
from collections import defaultdict
import re
from sys import argv
from os import path
import click

@click.command()
@click.option('--sam','-i', required=True, help="List of sam files 1 file per line.")
@click.option('--output','-o', required=True, help='Output file name for list of coverages.')
@click.option('--database', default="databases/WoL/wol_zebra_db.tsv", help='Database file with ncbi ids, taxon ids, genome lengths, and ncbi ids.')

def calculate_coverages(sam, output, database):
    ###################################
    #Calculate coverage of each contig#
    ###################################
    contig_dict = defaultdict(set)
    with open(sam_list,'r') as open_list_file:
        for samfile in open_list_file:
            with open(samfile.strip(), 'r') as open_sam_file:
                for line in open_sam_file:
                #Get values for contig, location, and length
                    linesplit= line.split()
                    contig = linesplit[2]
                    location = int(linesplit[3])
                    #Get sum of lengths in CIGAR string. Counting deleitons as alignment because they should be small
                    length_string = linesplit[5]
                    length = sum([int(x) for x in re.split("[a-zA-Z]",length_string) if x])
                    #Add range to contig_dict
                    for i in range(location,location+length):
                        contig_dict[contig].add(i)


    ###################################
    #Get information from database#
    ###################################
    ncbi_taxid_dict = dict()
    taxid_length_dict = dict()
    taxid_taxonomy_dict = dict()

    database_df = pd.read_csv(database, sep='\t')
    for i,line in database_df.iterrows():
        ncbi_taxid_dict[line.ncbi] = line.taxid
        taxid_length_dict[line.ncbi] = int(line.total_length)
        taxid_taxonomy_dict[line.taxid] = line.taxonomy

    ###funcitons to use helper information
    def get_taxid(x):
        return(ncbi_taxid_dict[x["ncbi_id"]])
    def get_taxonomy(x):
        return(taxid_taxonomy_dict[str(x.name)])
    def get_length(x):
        return(taxid_length_dict[str(x.name)])

    #####################
    #Calculate coverages#
    #####################
    #Make dataframe from dicitonary of coverages of each contig
    cov = pd.DataFrame({"ncbi_id":list(contig_dict.keys()),
                        "covered_length" : [len(x) for x in contig_dict.values()] } )
    #Merge contigs by taxid
    cov["taxid"] = cov.apply(func=get_taxid, axis=1)
    cov = cov.groupby("taxid").agg({"covered_length":sum})

    #Add total length of each taxid and calculate coverage percent
    cov["total_length"] = cov.apply(func=get_length, axis=1)
    cov["coverage_pct"] = cov.apply(func= lambda x : x["covered_length"]/x["total_length"], axis=1)

    #Add taxonomy and group taxids by taxonomy name. Take the max covered taxid for each taxonomy
    cov["taxonomy"] = cov.apply(func=get_taxonomy, axis=1)
    cov = cov.groupby("taxonomy").agg({"covered_length":"max","coverage_pct":"max"}).sort_values("coverage_pct",ascending=False)

    ##############
    #Write output#
    ##############
    cov.to_csv(output, sep='\t')

if __name__ == "__main__":
    calculate_coverages()
