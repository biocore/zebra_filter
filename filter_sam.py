#Get ncbi ids for taxa to remove

from collections import defaultdict
import click
import pandas as pd
from glob import glob
import sys
import os
import gzip
import lzma


def open_sam(samfile, mode):
    if samfile.endswith(".sam"):
        open_sam_file = open(samfile.strip(), mode)
    elif samfile.endswith(".sam.gz"):
        open_sam_file = gzip.open(
            samfile.strip(),
            mode=mode,
            encoding='utf-8')
    elif samfile.endswith(".sam.xz"):
        open_sam_file = lzma.open(
            samfile.strip(),
            mode=mode,
            encoding='utf-8')
    else:
        raise IOError("Unrecognized file extension on '%s'." % samfile)
    return open_sam_file


def open_files(in_file, out_file):
    in_fd = open_sam(in_file, "rt")
    out_fd = open_sam(out_file, "wt")
    return in_fd, out_fd

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

    sam_file_list = []
    sam_xz_file_list = []
    sam_gz_file_list = []
    if os.path.isdir(sam):
        sam_file_list = glob(sam + "/*.sam")
        sam_xz_file_list = glob(sam + "/*.sam.xz")
        sam_gz_file_list = glob(sam + "/*.sam.gz")
        if not sam_file_list and not sam_xz_file_list and not sam_gz_file_list:
            print("No sam files found in folder (.sam/.sam.xz/.sam.gz extensions required).")
            sys.exit(1)
    elif sam.endswith(".sam"):
        sam_file_list = [sam]
    elif sam.endswith(".sam.gz"):
        sam_gz_file_list = [sam]
    elif sam.endswith(".sam.xz"):
        sam_xz_file_list = [sam]
    else:
        print("Sam input requires either a sam file (with .sam/.sam.xz/.sam.gz extension) or a directory of sam files.")
        sys.exit(1)

    sam_file_list = sam_file_list + sam_gz_file_list + sam_xz_file_list

    # Create output directory if it doesn't exist
    if not os.path.exists(output):
        os.makedirs(output)

    #Get taxa to keep
    coverage_df = pd.read_table(input)
    taxa_to_keep = set(coverage_df.loc[coverage_df.coverage_ratio.astype(float) > cutoff, "gotu"])

    #Filter sam file(s)
    for i in range(len(sam_file_list)):
        in_file = sam_file_list[i]
        out_file = output + in_file.split('/')[-1].replace(".sam", '_filtered.sam')

        openin, openout = open_files(in_file, out_file)
        with openin, openout:
            for line in openin:
                if line.split('\t')[2] in taxa_to_keep:
                    openout.write(line)


if __name__ == "__main__":
    filter_sam()
