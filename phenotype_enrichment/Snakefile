# Ontologies and Set(s)
ARRAY_IDS = range(1,101,1)
JOIN_IDS = range(3,101,1)
ONTS = ["BP","GWAS","HPO","MP"]
SETS = ["ppn_pt"]
	
# Tool paths
python_path = "python3"

rule all:
	input:
		expand("enrichment/{set}_{ont}_enrichment.txt", ont=ONTS, set=SETS),
		expand("empiric_FDR/{set}_{ont}_empiric_FDR.txt", ont=ONTS, set=SETS)
					
rule gene_set_to_observed:
	input:
		"data/{set}_genes_with_3d_modifying_variants.txt"
	output:
		"observed/{set}_{ont}_observed.txt"
	params:
		python = python_path,
		mem = 30,
		time = "2:00:00",
		threads = 1
	shell:
		"{params.python} scripts/gene_set_to_observed.py --ontology {wildcards.ont} --set_name {wildcards.set}"
		
rule empiric_counts:
	input:
		"observed/{set}_{ont}_observed.txt"
	output:
		"empiric_counts/{set}_{ont}_empiric_counts_{array_ID}.txt"
	params:
		python = python_path,
		mem = 100,
		time = "12:00:00",
		threads = 1
	shell:
		"{params.python} scripts/empiric_counts.py --iterations 1000 --ontology {wildcards.ont} --set_name {wildcards.set} --array_id {wildcards.array_ID}"
		
rule concat_empiric_counts:
	input:
		expand("empiric_counts/{{set}}_{{ont}}_empiric_counts_{array_ID}.txt",array_ID=ARRAY_IDS),
		join = expand("empiric_counts/{{set}}_{{ont}}_empiric_counts_{join_ID}.txt", join_ID=JOIN_IDS)
	output:
		"empiric_counts/{set}_{ont}_empiric_counts.txt"
	params:
		mem = 30,
		time = "2:00:00",
		threads = 1
	run:
		if len(ARRAY_IDS) == 1:
			shell("cp empiric_counts/{wildcards.set}_{wildcards.ont}_empiric_counts_1.txt empiric_counts/{wildcards.set}_{wildcards.ont}_empiric_counts.txt")
		elif len(ARRAY_IDS) == 2:
			shell("join -t $'\t' empiric_counts/{wildcards.set}_{wildcards.ont}_empiric_counts_1.txt empiric_counts/{wildcards.set}_{wildcards.ont}_empiric_counts_2.txt > empiric_counts/{wildcards.set}_{wildcards.ont}_empiric_counts.txt")
		elif len(ARRAY_IDS) > 2:
			shell("join -t $'\t' empiric_counts/{wildcards.set}_{wildcards.ont}_empiric_counts_1.txt empiric_counts/{wildcards.set}_{wildcards.ont}_empiric_counts_2.txt > empiric_counts/{wildcards.set}_{wildcards.ont}.tmp")
			shell("for f in {input.join}; do join -t $'\t' empiric_counts/{wildcards.set}_{wildcards.ont}.tmp $f > empiric_counts/{wildcards.set}_{wildcards.ont}.tmpf && mv empiric_counts/{wildcards.set}_{wildcards.ont}.tmpf empiric_counts/{wildcards.set}_{wildcards.ont}.tmp; done")
			shell("mv empiric_counts/{wildcards.set}_{wildcards.ont}.tmp empiric_counts/{wildcards.set}_{wildcards.ont}_empiric_counts.txt")
			
rule calculate_enrichment:
	input:
		"empiric_counts/{set}_{ont}_empiric_counts.txt"
	output:
		"enrichment/{set}_{ont}_enrichment.txt"
	params:
		python = python_path,
		mem = 30,
		time = "2:00:00",
		threads = 1
	shell:
		"{params.python} scripts/enrichment.py --ontology {wildcards.ont} --set_name {wildcards.set}"
		
rule empiric_FDR:
	input:
		"enrichment/{set}_{ont}_enrichment.txt",
		"empiric_counts/{set}_{ont}_empiric_counts.txt"
	output:
		"empiric_FDR/{set}_{ont}_empiric_FDR.txt"
	params:
		python = python_path,
		mem = 60,
		time = "12:00:00",
		threads = 1
	shell:
		"{params.python} scripts/empiric_FDR.py --ontology {wildcards.ont} --set_name {wildcards.set} --subset_size 10000"
