#Get ncbi ids for taxa to remove

from collections import defaultdict
import click
import pandas as pd
from glob import glob
import sys
import os

@click.command()
@click.option('--input','-i', help='Input coverage .tsv file generated from Zebra.', required=True)
@click.option('--sam','-s', help='Sam file to filter or directory of sam files to filter.',required=True)
@click.option('--cutoff','-c', default=0.1, help='Minimum % genome coverage.', show_default=True)
@click.option('--database','-d', help='Database: tsv file with ncbi ids, taxon ids, genome lengths, and ncbi ids.', required=True)
@click.option('--output','-o', help='Output directory to write output files.', required=True)


def filter_sam(input, sam, cutoff, database, output):
    #Add / to end of output dir if not present
    output = output.rstrip('/') + '/'
    #Remove / from end of sam if present
    sam = sam.rstrip('/')
    if os.path.isdir(sam):
        sam_file_list=glob(sam + "/*.sam")
        if not sam_file_list:
            print("No sam files found in folder (.sam extensions required).")
            sys.exit(1)
    elif sam.split('.')[-1]=="sam":
        sam_file_list=[sam]
    else:
        print("Sam input requires either a sam file (with .sam extenstion) or a directory of sam files.")
        sys.exit(1)

    #Make output names
    sam_output_names = [output + file.split('/')[-1].replace(".sam",'_filtered.sam') for file in sam_file_list]

    #Make dictionary linking ncbi if to taxon name
    nucl_lineage_dict = defaultdict(list)
    #Load in database
    nucl_lineage_df = pd.read_csv(database, sep='\t')
    #Populate dictionary from database
    for i,line in nucl_lineage_df.iterrows():
        nucl_lineage_dict[line.taxon].extend(line.ncbi.split(','))

    #Get taxa to keep
    coverage_df = pd.read_csv(input, sep='\t')
    taxa_to_keep = set(coverage_df.loc[coverage_df.coverage_pct.astype(float) > cutoff, "taxonomy"])
    #Convert taxa_to_keep to ncbi_to_keep
    ncbi_to_keep=set()
    for taxon in taxa_to_keep:
        for ncbi in nucl_lineage_dict[taxon]:
            ncbi_to_keep.add(ncbi)

    #Filter sam file(s)
    for i in range(len(sam_file_list)):
        with open(sam_file_list[i], 'r') as openin, open(sam_output_names[i], 'w') as openout:
            for line in openin:
                if line.split('\t')[2] in ncbi_to_keep:
                    openout.write(line)

if __name__ == "__main__":
    filter_sam()
