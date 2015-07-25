#!/usr/bin/env python
import os

def process_reseq(basename, dirname_I, dirname_O, organism,
                  reference_dir='../reference/',population=False,breseq='breseq',
                  threads=2):
    '''Process DNA sequencing data from the command line
    
    Input:
    basename = base name of replicate fastq files
    dirname_I = name of the input directory holding the fastq files
    dirname_O = name of the output directory
    organism = e.g., NC_000913.3
    reference_dir = directory of the resequencing reference
    population = boolean, if true, the breseq polymorphism prediction will be used
                          if false, clonal resequencing (default)
    threads = the number of processors to use

    Output:
    
    Example usage:
    directories for this example: 
          /home/douglas/Documents/DNA_sequencing/fastq
          /home/douglas/Documents/DNA_sequencing/fastq/140818_11_OxicEvo04EcoliGlcM9_Broth-4 (sample 1 .fastq file locations)
          /home/douglas/Documents/DNA_sequencing/reference (.gbk file location)
          /home/douglas/Documents/DNA_sequencing/fastq/140818_11_OxicEvo04EcoliGlcM9_Broth-4 (output directory)
    
    at the terminal:
    cd /home/douglas/Documents/DNA_sequencing/fastq
    python3

    at the python command line:
    from resequencing_utilities.reseq import process_reseq
    process_reseq(...)
    '''

    # TODO: check to make sure that organism exists as a reference
    # TODO write docstring

    # parse the input
    #dirname, basename = os.path.split(base_input)
    base_input = dirname_I + basename;
    base_output = dirname_O + basename;
    if not dirname_I or len(dirname_I) == 0:
        dirname_I = ".";
    if not dirname_O:
        dirname_O = dirname_I;
    # files need to be extracted (fastq.gz should be deflated with gzip -d)
    fastq_files = [i for i in os.listdir(dirname_I)
            if i.startswith(basename) and i.endswith(".fastq")]
    f_str = " ".join(fastq_files);
    gbk_index = reference_dir + organism + ".gbk"

    # call breseq
    if population:
        breseq_cmd = ("%s -j %s -r %s -p %s"%(breseq,threads,gbk_index,f_str))
    else:
        breseq_cmd = ("%s -j %s -r %s %s"%(breseq,threads,gbk_index,f_str))
    print(breseq_cmd);
    os.system(breseq_cmd);