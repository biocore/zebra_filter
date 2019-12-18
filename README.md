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
```
Usage: calculate_coverages.py [OPTIONS]

Options:
  -i, --sam TEXT     List of sam files 1 file per line.  [required]
  -o, --output TEXT  Output file name for list of coverages.  [required]
  --database TEXT    Database file with ncbi ids, taxon ids, genome lengths,
                     and ncbi ids.
  --help             Show this message and exit.
```

### Filter sam files

```
Usage: filter_sam.py [OPTIONS]

Options:
  -i, --input TEXT     Input coverage .tsv file generated from Zebra.
                       [required]
  -s, --sam TEXT       Sam file to filter or directory of sam files to filter.
                       [required]
  -c, --cutoff FLOAT   Minimum % genome coverage.  [default: 0.1]
  -d, --database TEXT  File linking ncbi_id to taxonomy string.  [required]
  -o, --output TEXT    Directory to write output files.  [required]
  --help               Show this message and exit.
```
