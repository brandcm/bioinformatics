# get ancestral calls
wget -r -nH --cut-dirs=3 --no-parent -A.calls.txt.gz https://eichlerlab.gs.washington.edu/greatape/data/Ancestral_Alleles/
gzip -d chr*.calls.txt.gz

# get highest probability ancestral allele for node 18 into BED format
chrs=('chr1' 'chr2' 'chr3' 'chr4' 'chr5' 'chr6' 'chr7' 'chr8' 'chr9' 'chr10' 'chr11' 'chr12' 'chr13' 'chr14' 'chr15' 'chr16' 'chr17' 'chr18' 'chr19' 'chr20' 'chr21' 'chr22' 'chrX' )
for c in ${chrs[@]}; do awk '{print $1,$2-1,$2,$20}' OFS='\t' $c.calls.txt | tail -n +2 > $c.temp.bed; done
for c in ${chrs[@]}; do awk -F '/' '{print $1}' OFS='\t' $c.temp.bed > $c.bed; done
for c in ${chrs[@]}; do rm $c.temp.bed; done

# run through LiftOver, hg18 --> hg38

# concat separate files, remove rows with "?", sort, and resplit based on chromosome
cat chr*.bed > all_chrs_hg38.bed
awk '{print $1,$3,$4}' OFS='\t' all_chrs_hg38.bed > all_chrs_hg38.txt
grep -v "?" all_chrs_hg38.txt > filtered_all_chrs_hg38.txt
sort -V -k1,1 -k2,2 filtered_all_chrs_hg38.txt > sorted_filtered_all_chrs_hg38.txt
awk '{print>$1}' sorted_filtered_all_chrs_hg38.txt
for f in chr*; do mv $f $f.txt; done