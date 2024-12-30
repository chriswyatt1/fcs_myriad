# fcs_myriad

To get fcs running on myriad, complete the following steps:

1. Download the singularity image for fcs:

`curl https://ftp.ncbi.nlm.nih.gov/genomes/TOOLS/FCS/releases/latest/fcs-gx.sif -Lo fcs-gx.sif`
`singularity inspect fcs-gx.sif`  # check it works

2. Download the database (be aware, its 500GB):

`curl -LO https://github.com/peak/s5cmd/releases/download/v2.0.0/s5cmd_2.0.0_Linux-64bit.tar.gz`
`tar -xvf s5cmd_2.0.0_Linux-64bit.tar.gz`
`LOCAL_DB="/home/ucbtcdr/Scratch/fcs_scan"`
`./s5cmd  --no-sign-request cp  --part-size 50  --concurrency 50 s3://ncbi-fcs-gx/gxdb/latest/all.* $LOCAL_DB
  `

3. Download the fcs script:

`curl -LO https://github.com/ncbi/fcs/raw/main/dist/fcs.py`

4. Make a bash submission script:

```
#!/bin/bash -l
#$ -l h_rt=3:0:0
#$ -l mem=50G
#$ -wd /home/ucbtcdr/Scratch/fcs_scan
#$ -e /home/ucbtcdr/Scratch/fcs_scan

#Make an env variable where the image is:
export FCS_DEFAULT_IMAGE=/home/ucbtcdr/Scratch/fcs_scan/fcs-gx.sif  

#Run the fcs python script:
python3 ./fcs.py screen genome --fasta input/B_impatiens_GenomeSoftmasked.fa.gz --out-dir ./bombus_out/ --gx-db "/home/ucbtcdr/Scratch/fcs_scan" --tax-id 132113 
```

In the above, you need to specify the species tax ID (get this from NCBI or other DB).

# Replace contaminant regions with Ns

Use the python script to replace the contaminant or adaptor regions, when they represent just a small internal sequence and HiC shows that the two side either side of the contaminant are indeed connected:

## How to Use the Script:

Save the script to a file, e.g., replace_region.py. Make sure you chmod it, `chmod a+x replace_region.py`

Run the script from the command line with the required arguments:

`python replace_region.py input.fasta output.fasta HiC_scaffold_1 66580289 66614171`
input.fasta: Path to the input FASTA file.
output.fasta: Path to save the modified FASTA file.
HiC_scaffold_1: Name of the scaffold where the replacement will occur.
66580289: Start position of the region to replace (1-based).
66614171: End position of the region to replace (1-based).


