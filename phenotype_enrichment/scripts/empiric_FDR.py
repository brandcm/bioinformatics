import argparse
import numpy as np
import pandas as pd

def parse_args():
	parser = argparse.ArgumentParser()
	
	parser.add_argument(
		"--ontology", type=str, required=True, help="Name of ontology")

	parser.add_argument(
		"--set_name", type=str, required=True, help="Name of gene set")
		
	parser.add_argument(
		"--subset_size", type=int, help="Number of empiric counts to consider when calculating FDR")
		
	args = parser.parse_args()
	
	return args

def main():
	args = parse_args()
	f = open(f'empiric_counts/{args.set_name}_{args.ontology}_empiric_counts.txt')
	terms = f.readlines()
	out_df = []
	for term in terms:
		line = np.array(term.strip().split('\t'))
		name = line[0]
		if args.subset_size is not None:
			line = line[1:args.subset_size+1]
		else:
			line = line[1:]
		pvals = []
		for i, v in enumerate(line):
			if i % 10 == 0:
				print(i,flush=True)
			p = sum(line[:i] >= v) + sum(line[i+1:] >= v)
			p = (p+1)/len(line)
			pvals.append(p)
		out_df.append({**{'name': name},**dict(zip(range(len(pvals)),pvals))})
	out_df = pd.DataFrame(out_df)
	out_df.to_csv(f'empiric_FDR/{args.set_name}_{args.ontology}_empiric_FDR.txt', sep = '\t', header = None, index = None)

if __name__ == '__main__':
    main()