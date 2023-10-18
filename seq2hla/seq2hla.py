import os
import re
import subprocess
from Bio import SeqIO
from Bio.Blast import NCBIXML
from collections import defaultdict

this_file_path = os.path.dirname(os.path.abspath(__file__))
HLA_BLAST_DB = os.path.join(this_file_path, "..", "databases/hla_seqs/all_hla_seq.fasta")
FREQ_ALLELES_DB = os.path.join(this_file_path, "..", "databases/hla_freq/afnd.tsv")


def count_sequences_in_fasta(fasta_file):
    # Count the number of sequences in a FASTA file
    return sum(1 for record in SeqIO.parse(fasta_file, "fasta"))


def run_blastp(query_file, blast_db, blast_result_file, n_cpus=1):
    num_sequences = count_sequences_in_fasta(query_file)

    if num_sequences != 1:
        raise ValueError("Query file must contain exactly one sequence for blastp.")

    cmd = [
        'blastp',
        '-query',
        query_file,
        '-db',
        blast_db,
        '-out',
        blast_result_file,
        '-outfmt',
        '5',
        '-num_threads',
        str(n_cpus)
    ]

    try:
        subprocess.run(cmd, check=True)
        print(f"Blast command executed successfully for {query_file}.")
    except subprocess.CalledProcessError as e:
        print(f"An error occurred while executing blast: {e}")


def get_most_freq_allele_from_blastp_result(blastp_result_file):
    high_identity_matches = set()

    # Parse BLAST results and identify 100% identity matches
    with open(blastp_result_file) as result_handle:
        blast_records = NCBIXML.parse(result_handle)
        for blast_record in blast_records:
            for alignment in blast_record.alignments:
                for hsp in alignment.hsps:
                    if hsp.identities == hsp.align_length:
                        # 100% identity match
                        match = re.search(r'\w\*\d+:\d+', alignment.title)
                        if match:
                            high_identity_matches.add(match.group(0))

    # Read the frequency data and calculate mean alleles_over_2n
    allele_frequencies = defaultdict(list)
    with open(FREQ_ALLELES_DB) as afnd_file:
        next(afnd_file)  # Skip the header
        for line in afnd_file:
            fields = line.strip().split('\t')
            allele = fields[2]
            if allele in high_identity_matches: # Only consider high identity matches
                try:
                    alleles_over_2n = float(fields[5])
                except ValueError:
                    alleles_over_2n = float(fields[5].split('(*)')[0])
                allele_frequencies[allele].append(alleles_over_2n)

    # Calculate mean frequencies among populations
    mean_frequencies = {}
    for allele, frequencies in allele_frequencies.items():
        mean_frequencies[allele] = sum(frequencies) / len(frequencies)

    # Find the alleles with the highest mean frequency
    max_mean_frequency = max(mean_frequencies.values())
    highest_frequency_alleles = [allele for allele, mean_freq in
                                 mean_frequencies.items() if
                                 mean_freq == max_mean_frequency]

    return highest_frequency_alleles, mean_frequencies


def get_most_freq_allele_from_seq(fasta_file):
    blast_result_file = f"{fasta_file.split('.fasta')[0]}_blastp_result.xml"
    run_blastp(fasta_file, HLA_BLAST_DB, blast_result_file)
    highest_frequency_alleles, mean_frequencies =\
        get_most_freq_allele_from_blastp_result(blast_result_file)
    os.remove(blast_result_file)
    return highest_frequency_alleles, mean_frequencies

