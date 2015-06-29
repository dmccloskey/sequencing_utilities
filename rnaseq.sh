#!/bin/bash -l
#PBS -q serial
#PBS -N rnaseq_$FILENAME
#PBS -l walltime=02:00:00
#PBS -m abe

# USAGE: qsub rnaseq.sh -v FILENAME="NAME_OF_FILE_without_R1",ORGANISM="index_name"

if [ $PBS_O_WORKDIR ]
then
    cd $PBS_O_WORKDIR
fi

if [ $1 ]
then
    FILENAME=$1
fi

if [ $2 ]
then
    ORGANISM=$2
fi

SEQUTIL_DIR=$(python -c "import sequtil; print sequtil.seq_settings.sequtil_dir")
$SEQUTIL_DIR/rnaseq.py $FILENAME $ORGANISM
