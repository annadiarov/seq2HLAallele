import os
import requests
import subprocess

MOLECULE_TYPE = 'prot'
ALL_LOCI = ['A', 'B', 'C', 'DPA1', 'DPB1', 'DQA1', 'DQB1', 'DRB1']


def get_hla_seq_latest_version(output_dir):
    base_url = "https://raw.githubusercontent.com/ANHIG/IMGTHLA/Latest/fasta"

    for loci in ALL_LOCI:
        filename = f"{loci}_{MOLECULE_TYPE}.fasta"
        file_url = f"{base_url}/{filename}"
        out_file = os.path.join(output_dir, filename)

        response = requests.get(file_url)

        if response.status_code == 200:
            with open(out_file, "wb") as file:
                file.write(response.content)
        else:
            print(f"Failed to download. Status code: {response.status_code}")


def merge_hla_seq(output_dir, output_file):
    with open(output_file, 'w') as out_file:
        for loci in ALL_LOCI:
            filename = f"{loci}_{MOLECULE_TYPE}.fasta"
            file_path = os.path.join(output_dir, filename)

            with open(file_path, 'r') as in_file:
                for line in in_file:
                    out_file.write(line)


def make_blast_db(input_file):
    cmd = [
        'makeblastdb',
        '-in',
        input_file,
        '-dbtype',
        'prot',
        '-parse_seqids'
    ]

    try:
        subprocess.run(cmd, check=True)
        print(f"makeblastdb command executed successfully for {input_file}.")
    except subprocess.CalledProcessError as e:
        print(f"An error occurred while executing makeblastdb: {e}")


if __name__ == "__main__":
    this_file_path = os.path.dirname(os.path.abspath(__file__))
    databases_dir = os.path.join(this_file_path, '..', 'databases')
    output_dir = os.path.join(databases_dir, 'hla_seqs')
    os.makedirs(databases_dir, exist_ok=True)
    os.makedirs(output_dir, exist_ok=True)
    all_hla_seq_file = os.path.join(output_dir, 'all_hla_seq.fasta')
    get_hla_seq_latest_version(output_dir)
    merge_hla_seq(output_dir, all_hla_seq_file)
    make_blast_db(all_hla_seq_file)
    print('Successfully downloaded, merged and created a Blast DB of '
          'HLA sequences! \^o^/')
