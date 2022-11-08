# Colin M. Brand, University of California San Francisco, 05/25/2022

# This script adds variants to a reference sequence using separate variant and FASTA files per chromosome.

import argparse

def parse_args():
  parser = argparse.ArgumentParser()
	
	parser.add_argument(
		"--variants", type=str, required=True,
		help="Path to input text file with variants using 1-based coordinates. Text file should be tab-delimited and include the chromosome, position, and variant.")

	parser.add_argument(
		"--fasta", type=str, required=True,
		help="Path to input sequence in FASTA format.")
		
	parser.add_argument(
		"--out", type=str, required=True, help="Path to output FASTA file.")
		
	parser.add_argument(
		"--split", type=int, default=50, help="Number of bases by which to split new sequence. As with many FASTAs, the default is 50.")
		
	args = parser.parse_args()
	return args

def main():
	args = parse_args()

# make dictionary of variants
	dict = {}
	with open(args.variants, 'r') as calls:
		for site in calls:
			site = site.split()
			dict[int(site[1])] = site[2]
    
# write reference sequence with variant calls present in the dictionary
	with open(f'{args.fasta}', 'r') as fasta, open(f'{args.out}', 'w') as out:
		lines = [ line.strip() for line in fasta ]
		header = lines[0]
		print(header, file = out)
		no_header = lines[1:]
		seq = ''.join(no_header)

		for p, b in enumerate(seq, start=1):
			if p in dict:
				print(dict[p], end = "", file = out)
			else:
				print(b, end = "", file = out)
	
# read in output file to split the new sequence every nth base and rewrite output			
	with open(f'{args.out}', 'r') as out:
		lines = [ line.strip() for line in out ]
		header = lines[0]
		no_header = lines[1]
		seq = ''.join(no_header)
		
		new_seq = ''
		for i, bp in enumerate(seq):
			if i % args.split == 0:
				new_seq += '\n'
			new_seq += bp
			
		new_seq = new_seq[1:]
		
	with open(f'{args.out}', 'w') as out:
		print(header, file = out)
		print(new_seq, file = out) 

if __name__ == '__main__':
    main()
