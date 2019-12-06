#Get ncbi ids for taxa to remove

from collections import defaultdict
import click

@click.command()
@click.option('--input','-i', help='Input coverage .tsv file generated from Zebra.', required=True)
@click.option('--cutoff','-c', default=0.1, help='Minimum % genome coverage.')
@click.option('--nucl2lineage','-n', help='File linking ncbi_id to taxonomy string.',required=True)
@click.option('--output','-o', default="ids_to_exclude.txt", help='Name of output txt file.')

def get_taxa(input, cutoff, nucl2lineage, output):

    #Make dicitonary linking taxonomy to ncbi_id
    nucl_lineage_dict = defaultdict(list)
    with open(nucl2lineage, 'r') as openfile:
        for line in openfile:
            ncbi = line.split('\t')[0].strip()
            taxonomy = line.split('\t')[1].strip()
            nucl_lineage_dict[taxonomy].append(ncbi)

    #Make list of ncbi_ids to exclude
    out_ncbi_list = []
    #for line in coverage, add the ncbi_id of taxa that do not meet the genome coverage cutoff
    def process_line(line):

        coverage=float(line.split('\t')[2].strip())
        taxonomy=line.split('\t')[0].strip()
        if coverage < cutoff:

            out_ncbi_list.extend(nucl_lineage_dict[taxonomy])

    with open(input, 'r') as openfile:
        #Check for header line, and ignore if it doesn't work
        first_line= openfile.readline()
        try:
            process_line(line)
        except(ValueError, IndexError):
            pass
        for line in openfile:
            process_line(line)

    #Write the results to an output file. One ncbi_id per line.
    with open(output, 'w') as f:
        for ncbi in out_ncbi_list:
            f.write(ncbi + '\n')

if __name__ == "__main__":
    get_taxa()
