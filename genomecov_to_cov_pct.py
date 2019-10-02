

import pandas as pd
import numpy as np
from sys import argv


# Input 1: Bedtools genomecov file
cov_file = argv[1]

# Input 2: nucl2tid
nucl2tid_file = argv[2]

# input 3: nucl2lineage
nucl2lineage_file = argv[3]

# input 4: output file name
out_name = argv[4]

### Import bedtools coverage
#Don't filter out the zeros this time, because the header was trimmed down

cov =  pd.read_csv( cov_file, sep= '\t', header=None )
cov.rename(columns = {0: "ncbi_id", 1:"min_coverage", 2: "covered_length", 3: "total_length", 4:"coverage_pct"}, inplace=True)

#Get rid of the last two rows that contain the totals
cov = cov.iloc[:-2,]

### Import taxonomy
#nucl2tid file has info about which contigs belong to which genome
#nucl2lineage file to link ncbi_id to taxa string

ncbi_taxid_dict = dict()
ncbi_taxonomy_dict = dict()

with open(nucl2tid_file, 'r') as openfile:
    for line in openfile:
        ncbi = line.split()[0].strip()
        taxid = line.split()[1].strip()
        ncbi_taxid_dict[ncbi] = taxid
with open(nucl2lineage_file, 'r') as openfile:
    for line in openfile:
        ncbi = line.split()[0].strip()
        taxonomy = line.split()[1].strip()
        ncbi_taxonomy_dict[ncbi] = taxonomy

###Add taxid and taxonomy
def get_taxid(x):
    return(ncbi_taxid_dict[x["ncbi_id"]])
def get_taxonomy(x):
    return(ncbi_taxonomy_dict[x["ncbi_id"]])

cov["taxid"] = cov.apply(func=get_taxid, axis=1)
cov["taxonomy"] = cov.apply(func=get_taxonomy, axis=1)
def cap_at_10mb(x):
    if x["total_length"] > 10000000:
        return(10000000)
    else:
        return(x["total_length"])



### Merge by taxid and calculate coverage
#Some contigs have no cov=1 line and some have no cov=0 line. Need to groupby contig and take first to get cov of all
#Get length of each taxid
total_length_df = cov.groupby("ncbi_id").agg({"total_length":"first",
                           "taxid":"first"})
#Sum by taxid
total_length_df = total_length_df.groupby("taxid").agg({"total_length":"sum"})
#Cap at 10MB because around 60 taxid have multiple genomes. NEED TO FIX SOMEHOW
total_length_df["total_length"] = total_length_df.apply(cap_at_10mb, axis=1)
#Get length of coverage from lines with coverage=1
cov_cov = cov.loc[cov.min_coverage==1].groupby("taxid").agg({"taxonomy":"first","covered_length":"sum"})
#Merge
cov_cov = cov_cov.merge(total_length_df, left_index=True, right_index=True)
#Calculate coverage %
cov_cov["cov_pct"] = cov_cov.apply(lambda x: x["covered_length"]/ x["total_length"], axis=1)

#### Merge by taxonomy
# Taking theh maxinmum coverage pct for each taxa.
# Not sure how to keep covered length and total length because the max of those might be different than the max coverage percent

cov_cov_taxonomy = cov_cov.groupby("taxonomy").agg({"cov_pct":"max"}).sort_values("cov_pct",ascending=False)
cov_cov_taxonomy.to_csv(out_name, sep='\t')
