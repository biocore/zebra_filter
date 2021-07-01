filtered sample alignments can be generated using a threshold of 0.00085 (ie, take top 5 species from sample_output.tsv)

python ../filter_sam.py -i sample_output.tsv -s sample_alignments/ -c 0.00085 -o ./filtered_sample_alignments
