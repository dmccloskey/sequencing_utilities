#!/usr/bin/env python
import os

def process_reseq(base_input,orgnanism,population=False,breseq='breseq'):
    '''Process DNA sequencing data from the command line
    
    Input:
    base_input = list of sample directories for each replicate in sample 1
    organism = organism name

    Output:
    
    Example usage:
    directories for this example: 
          /home/douglas/Documents/RNA_sequencing/fastq
          /home/douglas/Documents/RNA_sequencing/fastq/140818_11_OxicEvo04EcoliGlcM9_Broth-4 (sample 1 .fastq file locations)
          /home/douglas/Documents/RNA_sequencing/indexes (.gtf file location)
          /home/douglas/Documents/RNA_sequencing/fastq/140818_11_OxicEvo04EcoliGlcM9_Broth-4 (output directory)
    
    at the terminal:
    cd /home/douglas/Documents/RNA_sequencing/fastq
    python3

    at the python command line:
    from resequencing_utilities.rnaseq import process_rnaseq
    run_cuffdiff()'''

    # TODO: check to make sure that organism exists as in index
    # TODO write docstring
    dirname, basename = os.path.split(base_input)
    if len(dirname) == 0:
        dirname = "."
    # files need to be extracted (fastq.gz should be deflated with gzip -d)
    fastq_files = [i for i in os.listdir(dirname)
            if i.startswith(basename) and i.endswith(".fastq")]
    gbk_index = indexes_dir + organism + ".gbk"

    #TODO
    '''gzip -d *.fastq.gz
    breseq -r $INDEXES_DIR/NC_000913.gbk `ls *.fastq`
    cd output
    ln -s ../data
    cd ..
    ln -s output $SAMPLENAME
    tar cf ../$SAMPLENAME.tar -h $SAMPLENAME
    rm $SAMPLENAME'''

    return