import pandas as pd
from collections import defaultdict
import re
from sys import argv
from os import path
import click
from glob import glob

@click.command()
@click.option('-i',"--input", required=True, help="Input: Directory of sam files (files must end in .sam).")
@click.option('-o',"--output", required=True, help='Output: file name for list of coverages.')
@click.option('-d',"--database", default="databases/WoL/metadata.tsv", help='WoL genome metadata file.',show_default=True)

def calculate_coverages(input, output, database):
    ###################################
    #Calculate coverage of each contig#
    ###################################
    gotu_dict = defaultdict(set)
    file_list = glob(input + "/*.sam")
    for samfile in file_list:
        with open(samfile.strip(), 'r') as open_sam_file:
            for line in open_sam_file:
            #Get values for contig, location, and length
                linesplit= line.split()
                gotu = linesplit[2]
                location = int(linesplit[3])
                #Get sum of lengths in CIGAR string. Counting deleitons as alignment because they should be small
                length_string = linesplit[5]
                length = sum([int(x) for x in re.split("[a-zA-Z]",length_string) if x])
                #Add range to contig_dict
                for i in range(location,location+length):
                    gotu_dict[gotu].add(i)
            print("Num GOTUs", len(gotu_dict))
            sumsize = 0
            for gotu in gotu_dict:
                sumsize += len(gotu_dict[gotu])
            print("Rough mem size:", sumsize)


    ###################################
    #Get information from database#
    ###################################
    md = pd.read_table(database).loc[:,["#genome","total_length","unique_name"]]
    md.columns = ["gotu","total_length","strain"]
    md = md.set_index("gotu")

    #####################
    #Calculate coverages#
    #####################
    #Make dataframe from dicitonary of coverages of each contig
    cov = pd.DataFrame({"gotu":list(gotu_dict.keys()),
                        "covered_length" : [len(x) for x in gotu_dict.values()] } )
    cov= cov.set_index("gotu")
    cov = cov.sort_values("covered_length", ascending=False)
    #Add genome metadata
    cov = cov.join(md, how="left")
    #Calculate coverage percent
    cov["coverage_ratio"] = cov.apply(func= lambda x : x["covered_length"]/x["total_length"], axis=1)
    cov = cov.loc[:,["covered_length","total_length","coverage_ratio","strain"]]

    ##############
    #Write output#
    ##############
    cov.to_csv(output, sep='\t')

if __name__ == "__main__":
    calculate_coverages()
