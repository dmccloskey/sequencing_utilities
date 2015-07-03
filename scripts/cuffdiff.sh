#!/bin/sh

SAMPLE1_1='/home/douglas/Documents/RNA_sequencing/fastq/140818_11_OxicEvo04EcoliGlcM9_Broth-4/140818_11_OxicEvo04EcoliGlcM9_Broth-4.bam'
SAMPLE1_2=''

SAMPLE2_1='/home/douglas/Documents/RNA_sequencing/fastq/140716_0_OxicEvo04pgiEcoliGlcM9_Broth-1/140716_0_OxicEvo04pgiEcoliGlcM9_Broth-1.bam'
SAMPLE2_2=''

#SAMPLE1=$SAMPLE1_1','$SAMPLE1_2
SAMPLE1=$SAMPLE1_1
SAMPLE1NAME='140818_11_OxicEvo04EcoliGlcM9_Broth-4'
#SAMPLE2=$SAMPLE2_1','$SAMPLE2_2
SAMPLE2=$SAMPLE2_1
SAMPLE2NAME='140716_0_OxicEvo04pgiEcoliGlcM9_Broth-1'

ORGANISM='ecoli_mg1655'
THREADS=12
OPTIONS='--library-type fr-firststrand --quartile-normalization --FDR 0.05 --num-threads '$THREADS
TRANSCRIPTS='/home/douglas/Documents/RNA_sequencing/indexes/'$ORGANISM'_notRNA_rRNA.gtf'

if [ $PBS_O_WORKDIR ]
then
    cd $PBS_O_WORKDIR
fi

echo cuffdiff -o $SAMPLE1NAME"_vs_"$SAMPLE2NAME $OPTIONS -L $SAMPLE1NAME,$SAMPLE2NAME $TRANSCRIPTS  $SAMPLE1 $SAMPLE2
cuffdiff -o $SAMPLE1NAME"_vs_"$SAMPLE2NAME $OPTIONS -L $SAMPLE1NAME,$SAMPLE2NAME $TRANSCRIPTS  $SAMPLE1 $SAMPLE2

#cuffdiff -o $SAMPLE1NAME"_vs_"$SAMPLE2NAME --library-type fr-firststrand --upper-quartile-norm --FDR 0.05 --num-threads $THREADS -L $SAMPLE1NAME,$SAMPLE2NAME ../indexes/$ORGANISM\_notRNA_rRNA.gtf `ls -1 $SAMPLE1*.bam | tr '\n' ','` `ls -1 $SAMPLE2*.bam | tr '\n' ','`
