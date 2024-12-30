import argparse
from Bio import SeqIO
from Bio.Seq import Seq

def replace_region_with_ns(fasta_file, output_file, scaffold, start, end):
    start -= 1  # Convert to 0-based index (Python uses 0-based indexing)
    with open(fasta_file, "r") as input_handle, open(output_file, "w") as output_handle:
        for record in SeqIO.parse(input_handle, "fasta"):
            if record.id == scaffold:
                sequence = list(str(record.seq))
                sequence[start:end] = ['N'] * (end - start)
                record.seq = Seq(''.join(sequence))  # Ensure record.seq is a Seq object
            SeqIO.write(record, output_handle, "fasta")

def main():
    parser = argparse.ArgumentParser(description="Replace a region in a FASTA file with Ns.")
    parser.add_argument("fasta_file", help="Input FASTA file")
    parser.add_argument("output_file", help="Output FASTA file")
    parser.add_argument("scaffold", help="Scaffold name to modify")
    parser.add_argument("start", type=int, help="Start position (1-based)")
    parser.add_argument("end", type=int, help="End position (1-based)")

    args = parser.parse_args()
    replace_region_with_ns(args.fasta_file, args.output_file, args.scaffold, args.start, args.end)

if __name__ == "__main__":
    main()
