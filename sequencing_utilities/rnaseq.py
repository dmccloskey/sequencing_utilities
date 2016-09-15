#!/usr/bin/env python
import os

#from .seq_settings import bowtie, indexes_dir, cufflinks
from .sam2bam import convert_samfile
from .makegff import write_samfile_to_gff


def process_rnaseq(basename, dirname_I, dirname_O, organism, indexes_dir='../indexes/', paired='paired', insertsize=1000, threads=8, trim3=3,
                   bowtie='bowtie',cufflinks='cufflinks',samtools='samtools',cuffdiff='cuffdiff',
                   htseqcount='htseq-count',htseqqa = 'htseq-qa',verbose_I=True,
                   library_type='fr-firststrand',index_type = '.gtf',
                   bowtie_options_I = '',cufflinks_options_I = ''):
    '''Process RNA sequencing data from the commandline

    Input:
    basename = base name of replicate fastq files
    dirname_I = name of the input directory holding the fastq files
    dirname_O = name of the output directory
    organism = organism name
    indexes_dir = directory of the bowtie indexes
    index_type = string, '.gtf' or '.gff'
    paired = 'paired', 'unpaired', or "mixed"
    library_type = string, cufflinks library type
    verbose_I = boolean
    bowtie_options_I = string, additional command line arguments not explicitly provided
    cufflinks_options_I = string, additional command line arguments not explicitly provided

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
    run_cuffdiff()

    '''
    # TODO: check to make sure that organism exists as in index
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
    if verbose_I: print(fastq_files);
    if index_type in ['.gtf','.gff']:
        gff_index = indexes_dir + organism + index_type
    else:
        print('index_type not recognized.')
    fna_index = indexes_dir + organism + ".fna"

    # generate the bowtie command based on input
    if paired=='paired':
        p1 = []
        p2 = []
        for fastq_file in fastq_files:
            name_part = fastq_file[len(basename):]
            # get rid of the ".fastq"
            name_part = name_part[:-6]
            if name_part.endswith("_001") or name_part.endswith("_000") or name_part.endswith("_002"):
                name_part = name_part[:-4]
            name_part = name_part.strip("_")
            if name_part == "R1":
                p1.append(dirname_I + fastq_file)
                #p1.append(fastq_file)
            elif name_part == "R2":
                p2.append(dirname_I + fastq_file)
                #p2.append(fastq_file)
        # TODO check to see if p1 and p2 are not empty
        assert(len(p1) == len(p2))
        assert(len(p1) > 0)
        p1.sort()
        p2.sort()
        p1_str = ",".join(p1)
        p2_str = ",".join(p2)
        if verbose_I: 
            print(p1_str);
            print(p2_str);
        #p1_str = dirname_O + "R1.fastq";
        #cat_files(p1,p1_str);
        #p2_str = dirname_O + "R2.fastq";
        #cat_files(p2,p2_str);
        # TODO -m 0
        #bowtie_command = "%s -X %d -n 2 -p %d -3 %d -S %s -1 %s -2 %s %s.sam" % \
        #    (bowtie, insertsize, threads, trim3, indexes_dir + organism, p1_str, p2_str, base_output)
        bowtie_options = "-X %d -n 2 -p %d -3 %d" % \
            (insertsize, threads, trim3)
        if bowtie_options_I:
            bowtie_options+=" %s" %(bowtie_options_I);
        bowtie_command = "%s %s -S %s -1 %s -2 %s %s.sam" % \
            (bowtie, bowtie_options, indexes_dir + organism, p1_str, p2_str, base_output)
    elif paired=='unpaired':
        p1 = []
        for fastq_file in fastq_files:
            name_part = fastq_file[len(basename):]
            # get rid of the ".fastq"
            name_part = name_part[:-6]
            if name_part.endswith("_001") or name_part.endswith("_000") or name_part.endswith("_002"):
                name_part = name_part[:-4]
            name_part = name_part.strip("_")
            if name_part == "R1":
                p1.append(dirname_I + fastq_file)
        assert(len(p1) > 0)
        p1.sort()
        p1_str = ",".join(p1)
        if verbose_I: 
            print(p1_str);
        #bowtie_command = "%s -n 2 -p %d -S %s %s %s.sam" % (bowtie, threads, indexes_dir + organism, p1_str, base_output)
        bowtie_options = "-n 2 -p %d -3 %d" % \
            (threads, trim3)
        if bowtie_options_I:
            bowtie_options+=" %s" %(bowtie_options_I);
        bowtie_command = "%s %s -S %s %s %s.sam" % (bowtie, bowtie_options, indexes_dir + organism, p1_str, base_output)
    elif paired=='mixed':
        p1 = []
        for fastq_file in fastq_files:
            name_part = fastq_file[len(basename):]
            # get rid of the ".fastq"
            name_part = name_part[:-6]
            if name_part.endswith("_001") or name_part.endswith("_000") or name_part.endswith("_002"):
                name_part = name_part[:-4]
            name_part = name_part.strip("_")
            if name_part == "R1":
                p1.append(dirname_I + fastq_file)
            elif name_part == "R2":
                p1.append(dirname_I + fastq_file)
        assert(len(p1) > 0)
        p1.sort()
        p1_str = ",".join(p1)
        if verbose_I: 
            print(p1_str);
        #bowtie_command = "%s -X %d -n 2 -p %d -3 %d --verbose -S %s --12 %s %s.sam" % \
        #    (bowtie, insertsize, threads, trim3, indexes_dir + organism, p1_str, base_output)
        bowtie_options = "-X %d -n 2 -p %d -3 %d" % \
            (insertsize, threads, trim3)
        if bowtie_options_I:
            bowtie_options+=" %s" %(bowtie_options_I);
        bowtie_command = "%s %s --verbose -S %s --12 %s %s.sam" % \
            (bowtie, bowtie_options, indexes_dir + organism, p1_str, base_output)

    # run the bowtie command
    print(bowtie_command)
    os.system(bowtie_command)

    # convert .sam to .bam for cufflinks
    convert_samfile(base_output + ".sam", sort=True, force=True, samtools=samtools,threads=threads)

    ## make a sorted samfile
    #os.system("%s view -h %s.bam > %s.unsorted.sam" % (samtools, base_output, base_output))
    #os.system("sort -k 1,1 %s.unsorted.sam > %s.sam" % (base_output, base_output))
    #os.system("%s -s reverse -i transcript_id %s.sam %s > %s.htseq_counts" % (htseqcount, base_output, gff_index, base_output))
    #os.system("%s %s.sam" % (htseqqa,base_output))
    
    # generate the cufflinks command and call cufflinks:
    #cufflinks_command = "%s --library-type %s -p %s -G %s -o %s/ %s.bam" % \
    #    (cufflinks, library_type, threads, gff_index, base_output,  base_output)
    cufflinks_options = "--library-type %s -p %s" % \
        (library_type, threads)
    if cufflinks_options_I:
        cufflinks_options+=" %s" %(cufflinks_options_I);
    cufflinks_command = "%s %s -G %s -o %s/ %s.bam" % \
        (cufflinks, cufflinks_options, gff_index, base_output,  base_output)
    print(cufflinks_command)
    os.system(cufflinks_command)

    # convert .bam to .gff
    write_samfile_to_gff(base_output + ".bam", base_output + ".gff", flip=True, separate_strand=True)

    # cleanup
    #os.system("rm %s.unsorted.sam" % (base_output))
    #os.system("rm %s.sam" % (base_output))
    #if p1_str and p2_str:
    #    os.system("rm %s" % (p1_str));
    #    os.system("rm %s" % (p2_str));

def cat_files(files_I,filename_O):
    """catenate file using the command prompt
    INPUT:
    files_I = list of file names
    filename_O = name of output file
    """
    cat1_cmd = "cat ";
    for file in files_I:
        cat1_cmd += file + " ";
    cat1_cmd += "> "+filename_O;

    print(cat1_cmd);
    os.system(cat1_cmd);

if __name__ == "__main__":
    from argparse import ArgumentParser
    parser = ArgumentParser("process RNAseq data")
    # TODO imporove documentation
    # TODO support non-paired end data
    parser.add_argument("name", help="""fastq filename. For paired end,
        include the filename up until _R1.fastq""")
    parser.add_argument("organism", help="""e_coli""")
    args = parser.parse_args()
    process_rnaseq(args.name, args.organism)
