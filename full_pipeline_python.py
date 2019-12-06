#Zebra filter full pipeline

from glob import glob
import pandas as pd
from collections import defaultdict
import re
from sys import argv
from os import path

#Input1 : sam file list
#Input2 : output name

#######################
#Check for input files#
#######################
try:
    sam_list = argv[1]
except IndexError:
    print("No input file list provided.")
    print("Input 1: txt file with list of sam files, 1 file per line.")
    print("Input 2: output file name.")
    print("Exiting.")
    exit()

try:
    out_name = argv[2]
except IndexError:
    print("No output name provided.")
    print("Input 1: txt file with list of sam files, 1 file per line.")
    print("Input 2: output file name.")
    print("Exiting.")
    exit()

if not path.exists(sam_list):
    print("Cannot locate input file list {}".format(sam_list))
    print("Exiting.")
    exit()

any_missing = False
with open(sam_list,'r') as openfile:
    for line in openfile:
        if not path.exists(line.strip()):
            print("Cannot locate input file: {}".format(line))
            any_missing=True

##############
#Helper files#
##############
# nucl2tid: link ncbi id to taxid
nucl2tid_file="/home/swandro/databases/nucl2tid.txt"

# nucl2lineage: link taxid to taxonomy
taxid2taxonomy_file="/home/swandro/databases/taxid2taxonomy.txt"

# taxid2length: link taxid to length
taxid_length_file="/home/swandro/databases/taxid2length.txt"

#Ensure all helper files exist
for file in [nucl2tid_file,taxid2taxonomy_file,taxid_length_file]:
    if not path.exists(file):
        print("Cannot locate helper file {}".format(file))
        any_missing=True

if any_missing:
    print("Exiting.")
    exit()

#####################
#Calculate coverages#
#####################

def make_contig_dict():
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
    return(contig_dict)


###################################
#Get information from helper files#
###################################
ncbi_taxid_dict = dict()
taxid_length_dict = dict()
taxid_taxonomy_dict = dict()

with open(nucl2tid_file, 'r') as openfile:
    for line in openfile:
        ncbi = line.split()[0].strip()
        taxid = line.split()[1].strip()
        ncbi_taxid_dict[ncbi] = taxid

with open(taxid_length_file, 'r') as openfile:
    openfile.readline()
    for line in openfile:
        ncbi = line.split()[0].strip()
        length = line.split()[1].strip()
        taxid_length_dict[ncbi] = int(length)

with open(taxid2taxonomy_file, 'r') as openfile:
    for line in openfile:
        taxid = line.split()[0].strip()
        taxonomy = line.split()[1].strip()
        taxid_taxonomy_dict[taxid] = taxonomy

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
cov.to_csv(out_name, sep='\t')
