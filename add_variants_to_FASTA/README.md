## Add Variants to FASTA

This directory contains a script that adds variants to a reference sequence in FASTA file format. There are multiple extant programs that can complete this task (e.g., bcftools consensus, GATK FastaAlternateReferenceMaker). However, such programs require software and strict input file formats for variants. This script here requires only Python version 3 and the input variant file is a text file that can be easily edited. As currently written, the script should be run separately per chromosome/contig requiring separate files for the sequence and variants. Sequence files should be uncompressed. I have included bash code below to perform this task across multiple chromosomes.

Also present in this directory are two example files that can be used to see the script in action. 'example_variants.txt' illustrates the variant file format, which includes three tab-delimited fields: chromosome, variant position (1-based), and the variant to be inserted. 'example_FASTA.fa' is an example FASTA. To generate a new FASTA using the example reference and example variants, run the following:

```
python add_variants_to_FASTA.py --variants example_variants.txt --fasta example_FASTA.fa --out new_FASTA.fa
```

The resulting sequence should be: TAACNCTAACCCNAACCCTNACCNA.

<br/>

### Multiple Chromosomes

To run this script across multiple chromosomes and generate a single, multi-chromosome FASTA, I recommend naming the variant and FASTA files by the chromosome and running this command.

```
chrs=('chr1' 'chr2' 'chr3' 'chr4' 'chr5' 'chr6' 'chr7' 'chr8' 'chr9' 'chr10' 'chr11' 'chr12' 'chr13' 'chr14' 'chr15' 'chr16' 'chr17' 'chr18' 'chr19' 'chr20' 'chr21' 'chr22' 'chrX' 'chrY' 'chrM' )

for chr in ${chrs[@]}; do python add_variants_to_FASTA.py --variants "$chr"_variants.txt --fasta "$chr".fa --out new_"$chr".fa; done
cat new_*.fa > new_sequence.fa
```

<br/>

I also highly recommend indexing your new FASTA file using samtools faidx. If your variants are in a VCF file, one can use bcftools query to extract the necessary fields. Additionally, if you find yourself starting with multi-chromosomal files at the onset, here are a few ways to generate chromosome-specific files.

1) For the variant file, use the command below to split by the first field (chromosome) using awk. This assumes that the chromosome field includes "chr" before the chromosome number.

```
awk '{print>$1}' all_variants.txt && for c in chr*; do mv $c $c_variants.txt; done
```

<br/>

2) For the FASTA file, one can use a tool like samtools to split a FASTA:

```
chrs=('chr1' 'chr2' 'chr3' 'chr4' 'chr5' 'chr6' 'chr7' 'chr8' 'chr9' 'chr10' 'chr11' 'chr12' 'chr13' 'chr14' 'chr15' 'chr16' 'chr17' 'chr18' 'chr19' 'chr20' 'chr21' 'chr22' 'chrX' 'chrY' 'chrM' )

for chr in ${chrs[@]}; do samtools faidx input.fa "$chr" > "$chr".fa; done
```

<br/>

Alternatively, one could easily download chromosome-specific files from a repository such as hg19 from UCSC:

```
chrs=('chr1' 'chr2' 'chr3' 'chr4' 'chr5' 'chr6' 'chr7' 'chr8' 'chr9' 'chr10' 'chr11' 'chr12' 'chr13' 'chr14' 'chr15' 'chr16' 'chr17' 'chr18' 'chr19' 'chr20' 'chr21' 'chr22' 'chrX' 'chrY' 'chrM' )

for chr in ${chrs[@]}; do wget https://hgdownload.soe.ucsc.edu/goldenPath/hg19/chromosomes/"$chr".fa.gz; done
for chr in ${chrs[@]}; do gunzip "$chr".fa.gz; done
```
