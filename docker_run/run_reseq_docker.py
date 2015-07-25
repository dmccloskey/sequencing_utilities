#!/usr/bin/env python
import os
import csv, sys, json

def run_reseq_docker():
    """processing resequencing data using docker"""

    #TODO: in docker run file
    '''gzip -d *.fastq.gz
    breseq -r $INDEXES_DIR/NC_000913.gbk `ls *.fastq`
    cd output
    ln -s ../data
    cd ..
    ln -s output $SAMPLENAME
    tar cf ../$SAMPLENAME.tar -h $SAMPLENAME
    rm $SAMPLENAME'''

if __name__ == "__main__":
    #TODO
    from argparse import ArgumentParser
    parser = ArgumentParser("process RNAseq data")
    parser.add_argument("basename_I", help="""base name of the fastq files""")
    parser.add_argument("host_dirname_I", help="""directory for .fastq files""")
    parser.add_argument("organism_I", help="""name of index""")
    parser.add_argument("host_reference_dir_I", help="""directory for reference""")
    parser.add_argument("local_dirname_I", help="""location for temporary output""")
    parser.add_argument("host_dirname_O", help="""location for output on the host""")
    parser.add_argument("threads_I", help="""number of processors to use""")
    args = parser.parse_args()
    run_rnaseq_docker(args.basename_I,args.host_dirname_I,args.organism_I,args.host_indexes_dir_I,
                      args.local_dirname_I,args.host_dirname_O,
                      args.threads_I);