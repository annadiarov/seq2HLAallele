# seq2HLAallele

This package is designed to address the challenge of allele typing for HLA genes
in crystallography, even when the available sequences are incomplete. 
It leverages the BLAST tool to identify the closest matching allele within the 
HLA database. Subsequently, it calculates the mean frequency of alleles_over_2n 
across diverse populations, enabling the determination of the most probable allele.
Finally, it outputs the matched allele with highest frequency in the standard
HLA nomenclature.

The format of the output allele will follow the [HLA Naming](https://hla.alleles.org/nomenclature/naming.html 
): 
```
HLA<gene>*<allele_group>:<specific_HLA_protein>
```

## Installation
### Environment
Create a python 3.11 environment and install the requirements:
```bash
conda create -n seq2hla python=3.11
conda activate seq2hla
pip install -r requirements.txt
```
Make sure your computer has installed blast tools. If not, you can install it by:
```bash
sudo apt install ncbi-blast+
```
### Download databases
You have to download the HLA sequence database and the HLA frequencies database
before using the package.

The database files should be under the `databases/` folder with the following
structure:
```
- databases/
   |-> hla_freq/
   |     - afnd.tsv
   |-> hla_seqs/
        - A_prot.fasta
        - all_hla_seq.fasta
        - B_prot.fasta
        - C_prot.fasta
        - DPA1_prot.fasta
        - DPB1_prot.fasta
        - DQA1_prot.fasta
        - DQB1_prot.fasta
        - DRB1_prot.fasta
```

##### HLA sequence database
You can also download the database latest version and create the Blast DB
automatically with:
```bash
python seq2hla/download_imgthla_database.py
```

Alternatively, you can download the HLA database of HLA amino acid sequences from
[IMGT/HLA](https://github.com/ANHIG/IMGTHLA/tree/Latest/).
The files should be under the `fasta/*_prot.fasta`. 
Unify them in a single file
called `all_hla_seq.fasta` and place it under the `databases/hla_seqs/` folder.
Then execute the command:
```bash
makeblastdb -in databases/hla_seqs/all_hla_seq.fasta -dbtype prot -parse_seqids
```

##### HLA frequencies database
You can manually download the file `afnd.tsv` HLA frequencies database from this 
[GitHub Repo](https://github.com/slowkow/allelefrequencies/tree/main) and place
it under the `databases/hla_freq/` folder.

You can also download the database latest version automatically using the code 
provided by this [GitHub Repo](https://github.com/slowkow/allelefrequencies/tree/main):
```bash
python seq2hla/download_imgthla_database.py
```
> **Warning**: This download my take ~1-2 hours. 

As an alternative, you can directly download the file `afnd.tsv` from the
repo using the flag `--fast` (or `-f`):
```bash
python seq2hla/download_allele_freq_database.py --fast
```


