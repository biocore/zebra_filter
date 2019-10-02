import sys
from collections import defaultdict

#Outputs a trimmed .sam header with only the ncbi ID of taxa present

#INPUTS
#1 : File with full header
header_file = sys.argv[1]
#2 : List of ncbi IDs for sequences to keep
# Get this from the sorted samfile with: cut -f3 file.sam | uniq > seqs_keep.txt
seqs_keep_file = sys.argv[2]
#3: File with ncbi taxonomy nucl2lineage.txt
taxid_file = sys.argv[3]
#4 : Name of output header
outfile = open(sys.argv[4], 'w')

ncbi_tax_dict = dict()
tax_ncbi_dict = defaultdict(list)
done_tax = set()
ncbi_to_output = set()

#Get dictionaries for converting between ncbi and taxid
with open(taxid_file, 'r') as openfile:
    for line in openfile:
        ncbi = line.split()[0].strip()
        taxid = line.split()[1].strip()
        ncbi_tax_dict[ncbi] = taxid
        tax_ncbi_dict[taxid].append(ncbi)

#Get list of ncbi to keep
with open(seqs_keep_file, 'r') as openfile:
    for line in openfile:
        #For each ncbi
        ncbi = line.strip()
        #Get the Taxid
        taxid = ncbi_tax_dict   [ncbi]
        #If the taxid has not been done
        if taxid not in done_tax:
            #Get the list of ncbi associated with that taxid
            ncbi_to_add = tax_ncbi_dict[taxid]
            #Add each ncbi to the final list of ncbi to output
            for item in ncbi_to_add:
                ncbi_to_output.add(item)
            #Add the taxid to the set of finished taxids
            done_tax.add(taxid)


#Go through the old header and output the ones in the list of keepers
with open(header_file, 'r') as openfile:
    for line in openfile:
        ncbi = line.split()[1].split(":")[1].strip()
        if ncbi in ncbi_to_output:
            outfile.write(line)
