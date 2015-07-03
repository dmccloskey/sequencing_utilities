#!/bin/bash -l
#PBS -q serial
#PBS -N cuffdiff_$SAMPE1NAME\_$SAMPLE2NAME
#PBS -l walltime=03:00:00
#PBS -m abe

# USAGE: qsub cuffdiff.sh -v SAMPLE1="bamfile_base",SAMAPLE1NAME="s1",SAMPLE2="bamfile_base",SAMPLE2NAME="s2",ORGANISM="index_name",THREADS="#ofThreads"

if [ $PBS_O_WORKDIR ]
then
    cd $PBS_O_WORKDIR
fi

echo cuffdiff -o $SAMPLE1NAME"_vs_"$SAMPLE2NAME --library-type fr-firststrand --quartile-normalization --FDR 0.05 --num-threads $THREADS -L $SAMPLE1NAME,$SAMPLE2NAME ../indexes/$ORGANISM\_notRNA_rRNA.gtf `ls -1 $SAMPLE1 | tr '\n' ','` `ls -1 $SAMPLE2 | tr '\n' ','`

#cuffdiff -o $SAMPLE1NAME"_vs_"$SAMPLE2NAME --library-type fr-firststrand --upper-quartile-norm --FDR 0.05 --num-threads $THREADS -L $SAMPLE1NAME,$SAMPLE2NAME ../indexes/$ORGANISM\_notRNA_rRNA.gtf `ls -1 $SAMPLE1*.bam | tr '\n' ','` `ls -1 $SAMPLE2*.bam | tr '\n' ','`
