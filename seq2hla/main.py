import sys
from seq2hla import get_most_freq_allele_from_seq

def usage():
    print("Usage: python main.py <in_fasta>")
    print("Example: python main.py example.fasta")
    sys.exit(1)


if __name__ == "__main__":
    in_fasta = sys.argv[1]
    if in_fasta == "-h" or in_fasta == "--help":
        usage()
    high_freq_alleles, mean_freq = get_most_freq_allele_from_seq(in_fasta)
    print("Alleles with the highest mean frequency:")
    for allele in high_freq_alleles:
        print(f"\t{allele}\tMean Frequency: {mean_freq[allele]}")
