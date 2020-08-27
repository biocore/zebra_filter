#Get ncbi ids for taxa to remove

from collections import defaultdict
import click
import pandas as pd
from glob import glob
import sys
import os

@click.command()
@click.option('--input','-i', help='Input coverage .tsv file generated from calculate_coverages.py.', required=True)
@click.option('--sam','-s', help='Sam file to filter or directory of sam files to filter.',required=True)
@click.option('--cutoff','-c', default=0.1, help='Minimum % genome coverage.', show_default=True)
@click.option('--output','-o', help='Output directory to write output files. Will be created if does not exist.', required=True)


def filter_sam(input, sam, cutoff, output):
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
    #Create output directory if it doesn't exist
    if not os.path.exists(output):
        os.makedirs(output)
    #Make output names
    sam_output_names = [output + file.split('/')[-1].replace(".sam",'_filtered.sam') for file in sam_file_list]

    #Get taxa to keep
    coverage_df = pd.read_table(input)
    taxa_to_keep = set(coverage_df.loc[coverage_df.coverage_ratio.astype(float) > cutoff, "gotu"])

    #Filter sam file(s)
    for i in range(len(sam_file_list)):
        with open(sam_file_list[i], 'r') as openin, open(sam_output_names[i], 'w') as openout:
            for line in openin:
                if line.split('\t')[2] in taxa_to_keep:
                    openout.write(line)

if __name__ == "__main__":
    filter_sam()
