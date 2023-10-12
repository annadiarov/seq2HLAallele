import os
import requests

MOLECULE_TYPE = 'prot'
ALL_LOCI = ['A', 'B', 'C', 'DMA', 'DMB', 'DOA', 'DOB', 'DPA1', 'DPB1',
            'DQA1', 'DQA2', 'DQB1', 'DQB2', 'DRA', 'DRB1', 'DRB345', 'DRB']


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


if __name__ == "__main__":
    this_file_path = os.path.dirname(os.path.abspath(__file__))
    output_dir = os.path.join(this_file_path, '..', 'databases', 'hla_seqs')
    all_hla_seq_file = os.path.join(output_dir, 'all_hla_seq.fasta')

    get_hla_seq_latest_version(output_dir)
    merge_hla_seq(output_dir, all_hla_seq_file)
    print('Successfully downloaded and merged HLA sequences! \^o^/')
