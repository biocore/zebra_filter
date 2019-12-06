# zebra_filter
Filtering out false taxonomic hits from shotgun sequencing based on aggregated genome coverage.  
For usage on .sam alignment files of shotgun sequencing reads, such as those from SHOGUN.  

Step 1: Aggregate the % genome coverage of each species in all samples.
- Output: List of % genome coverage for each species.   
Step 2: Filter out alignments to low coverage genomes from the sam files
- Output: sam files with fewer false positives.

Then biom tables can be generated from those sam alignments using SHOGUN or gOTUs.

## Usage

### Calculate coverages  
Input: txt file list of sam files locations. 1 file per line
Output: tsv file list of aggregated coverage % per hit genome 

python full_pipeline_python.py sam_list.txt coverage_output.tsv


### Filter sam files
Input: Coverage tsv generated from previous step and sam files
Output: Filtered sam files

First, choose a coverage cutoff and get the list of ncbi ids to filter from the sam alignments.
python get_ncbi_to_exclude_from_coverages.py -i coverage_output.tsv -c 0.1 -o ids_to_filter.txt

Second, use the list of ncbi ids to filter to filter the sam files.
python filter_sam.py -s alignment.sam -f ids_to_filter.txt -o filtered_alignment.sam


