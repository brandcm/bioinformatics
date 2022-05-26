# Colin M. Brand, University of California San Francisco, 05/25/2022

import argparse

def parse_args():
	parser = argparse.ArgumentParser()
	
	parser.add_argument(
		"--ancestral", type=str, required=True,
		help="Path to input text file with ancestral alleles. Text file should be tab-delimited and include the chromosome, position, and ancestral allele.")

	parser.add_argument(
		"--reference", type=str, required=True,
		help="Name of input reference sequences in FASTA format.")
		
	parser.add_argument(
		"--out", type=str, required=True, help="Name of output FASTA file.")
		
	args = parser.parse_args()
	return args

def main():
	args = parse_args()

# make dictionary of ancestral alleles
	dict = {}
	with open(args.ancestral, 'r') as calls:
		for site in calls:
			site = site.split()
			dict[int(site[1])] = site[2]
    
# write reference sequence with ancestral calls present in the dictionary
	with open(f'{args.reference}.fa', 'r') as fasta, open(f'{args.out}.fa', 'w') as out:
		lines = fasta.readlines()
		header = lines[0]
		header = header.strip()
		print(header, file = out)
		no_header = lines[1:]
		seq = ''.join(no_header)
	
		for p, b in enumerate(seq, start=1):
			if p in dict:
				print(dict[p], end = "", file = out)
			else:
				print(b, end = "", file = out)

if __name__ == '__main__':
    main()