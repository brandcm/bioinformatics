import argparse
import random
import pandas as pd
import pybedtools

def parse_args():
	parser = argparse.ArgumentParser()

	parser.add_argument(
		"--iterations", type=int, required=True, default=1000, help="Number of observations to generate")
	
	parser.add_argument(
		"--ontology", type=str, required=True, help="Name of ontology")
	
	parser.add_argument(
		"--set_name", type=str, required=True, help="Name of variant set being considered")
		
	parser.add_argument(
		"--array_id", type=int, required=True, default=0, help="Array ID to use if parallelizing")
					
	args = parser.parse_args()
	
	return args

# other input files
genes = pybedtools.BedTool('data/panTro6_genes.bed')
TADs_file = pd.read_csv('data/merged_panTro6_TADs.bed', sep = '\t', header = None)
TADs = pybedtools.BedTool.from_dataframe(TADs_file)

def main():
	args = parse_args()
	set = args.set_name
	ontology = get_ontology(set)
	ontology_empiric = []
	while len(ontology_empiric) < args.iterations:
	    gene_counts = shuffle_and_count(ontology)
	    if gene_counts is not None:
	    	ontology_empiric.append(gene_counts)
	ontology_empiric_df = pd.DataFrame(ontology_empiric).T
	ontology_empiric_df.to_csv(f'empiric_counts/{args.set_name}_{args.ontology}_empiric_counts_{args.array_id}.txt', header = False, index = True, sep = '\t')

def get_ontology(set):
	args = parse_args()
	observed_ontology_df = pd.read_csv(f'observed/{args.set_name}_{args.ontology}_observed.txt', sep='\t', index_col=0)
	terms = list(observed_ontology_df.index[observed_ontology_df.sum(axis=1) > 0])
	ontology = {}
	file = open(f'ontologies/{args.ontology}.txt', 'r')
	lines = file.readlines()
	for line in lines:
		line = line.strip().split("\t")
		if args.ontology + ": " + line[0] in terms:
			ontology[args.ontology + ": " + line[0]] = line[2:]
	file.close()
	return ontology

def shuffle_and_count(ontology):
	variants_file = pd.read_csv('data/ppn_pt_3d_modifying_variants.bed', sep = '\t', header = None)
	variants = pybedtools.BedTool.from_dataframe(variants_file)
	shuffled_variants = variants.shuffle(g = 'data/panTro6_chr_lengths.txt', incl = 'data/panTro6_windows_with_full_coverage.bed')
	intersect = TADs.intersect(shuffled_variants, wo = True).intersect(genes, loj = True).to_dataframe(disable_auto_names=True, header=None)
	shuffled_genes = list([x for x in intersect[11] if str(x) != '.'])
	gene_counts = {}
	for i,r in ontology.items():
		gene_counts[i] = 0
		for g in shuffled_genes:
			if g in r:
				gene_counts[i]+=1
	return gene_counts
	
if __name__ == '__main__':
    main()
