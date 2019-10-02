### Automated workflow

module load bedtools_2.26.0

#Input bowtie2 sam alignment from shogun
in_sam=$1
out_name=$2

#Required paths
nucl2tid="/home/swandro/databases/nucl2tid.txt"
nucl2nucl="/home/swandro/databases/nucl2lineage_fixed.txt"
index="/home/swandro/databases/nucl.fna.fai"
filter_header_python="/home/swandro/scripts/filter_header_new.py"
genomecov_to_cov_pct_python="/home/swandro/scripts/genomecov_to_cov_pct.py"
full_header="/home/swandro/false_hit_filtering/full_pipeline/full_header.sam"

#Get all the sequence hits in all the files
for file in $in_sam/*.sam
  do
    cut -f3 $file >> temp_seqs_keep.txt
  done
#Get the unique hits
sort temp_seqs_keep.txt | uniq > temp_seqs_keep_uniq.txt

echo "Filtering header"
#Filter header (while keeping all ncbi id of taxa with any coverage)
python $filter_header_python \
$full_header \
temp_seqs_keep_uniq.txt \
$nucl2tid \
temp_filtered_header.txt

echo "Adding filtered header to alignment"
#Add filtered header to alignment

cat temp_filtered_header.txt $in_sam/*.sam | samtools view -bu - | samtools sort - > temp_alignment_filtered_header.bam

echo "Calculating genomecov"
# Use bedtools to calculate coverage
bedtools genomecov -ibam temp_alignment_filtered_header.bam -max 1 > temp_coverages.tsv


echo "Parsing genomecoverage"
#Calculate the coverage percent of each taxa
python $genomecov_to_cov_pct_python \
temp_coverages.tsv \
$nucl2tid \
$nucl2nucl \
$out_name

echo "Cleaning up"

#rm temp_all_header.sam temp_seqs_keep.txt temp_just_header.txt \
#temp_alignment.sam temp_filtered_header.txt temp_alignment_filtered_header.bam \
#temp_coverages.tsv temp_seqs_keep_uniq.txt

echo "Finished!"
