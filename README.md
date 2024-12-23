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