#!/bin/bash -l
#PBS -q serial
#PBS -N reseq_$SAMPLENAME
#PBS -l nodes=1:ppn=1,walltime=07:02:00
#PBS -m abe

# USAGE: qsub reseq.sh -vSAMPLENAME="DIRECTORY_NAME_OF_SAMPLE"

if [ $PBS_O_WORKDIR ]
then
    cd $PBS_O_WORKDIR
fi

if [ -z "$SAMPLENAME" ]
then
    SAMPLENAME=$1
fi

echo $SAMPLENAME
cd $SAMPLENAME

INDEXES_DIR=$(python -c "import sequtil; print sequtil.seq_settings.indexes_dir")

gzip -d *.fastq.gz
breseq -r $INDEXES_DIR/NC_000913.gbk `ls *.fastq`
cd output
ln -s ../data
cd ..
ln -s output $SAMPLENAME
tar cf ../$SAMPLENAME.tar -h $SAMPLENAME
rm $SAMPLENAME
