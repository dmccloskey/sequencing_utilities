from pandas import read_table
import os

def load_cuffdiff(filename):
    if os.path.isdir(filename):
        filename = os.path.join(filename, "isoform_exp.diff")
    table = read_table(filename, index_col="test_id",
        true_values=["yes"], false_values=["no"])
    table = table.rename(columns={"log2(fold_change)": "fold_change"})
    
    return table

def run_cuffdiff(samples_dir_1,samples_dir_2,sample_name_1,sample_name_2,organism,output_dir,
                   cuffdiff='cuffdiff',indexes_dir='../indexes/', threads = 1,
                   library_norm_method = 'quartile', fdr = 0.05,
                   library_type ='fr-firststrand',
                   more_options=None):
    '''Run cuffdiff from the commandline

    Input:
    samples_dir_1 = list of sample directories for each replicate in sample 1
    samples_dir_2 = list of sample directories for each replicate in sample 2
    samples_name_1 = sample name for sample 1
    samples_name_1 = sample name for sample 2
    organism = organism name
    output_dir = directory of cuffdiff output
    cuffdiff = string to run cuffdiff (give the absolute directory of cuffdiff.exe if cuffdiff is not in PATH)
    indexes_dir = directory where indexes are located
    library_type = string indicating the library type (e.g. fr-first-strand)
    more_options = other options not specified (e.g. '--library-type fr-firststrand)

    Output:
    
    Example usage:
    directories for this example: 
          /home/douglas/Documents/RNA_sequencing/fastq
          /home/douglas/Documents/RNA_sequencing/fastq/140818_11_OxicEvo04EcoliGlcM9_Broth-4 (sample 1 .bam file locations)
          /home/douglas/Documents/RNA_sequencing/fastq/140716_0_OxicEvo04pgiEcoliGlcM9_Broth-1 (sample 2 .bam file locations)
          /home/douglas/Documents/RNA_sequencing/indexes (.gtf file location)
          /home/douglas/Documents/RNA_sequencing/fastq/ (output directory) 
    
    at the terminal:
    cd /home/douglas/Documents/RNA_sequencing/fastq
    python3

    at the python command line:
    from resequencing_utilities.cuffdiff import run_cuffdiff
    run_cuffdiff(['/home/douglas/Documents/RNA_sequencing/fastq/140818_11_OxicEvo04EcoliGlcM9_Broth-4/140818_11_OxicEvo04EcoliGlcM9_Broth-4.bam'],
        ['/home/douglas/Documents/RNA_sequencing/fastq/140716_0_OxicEvo04pgiEcoliGlcM9_Broth-1/140716_0_OxicEvo04pgiEcoliGlcM9_Broth-1.bam'],
        '140818_11_OxicEvo04EcoliGlcM9_Broth-4','140716_0_OxicEvo04pgiEcoliGlcM9_Broth-1',
        'ecoli_mg1655',
        '/home/douglas/Documents/RNA_sequencing/fastq/',
        threads = 48)

    '''
    
    # parse input into string values
    sample_1=','.join(samples_dir_1);
    sample_2=','.join(samples_dir_2);

    gff_index = indexes_dir + organism + ".gtf";

    cuffdiff_options = "--library-type %s --library-norm-method %s --FDR %s --num-threads %s" % \
        (library_type,library_norm_method,fdr,threads);
    if more_options:
        cuffdiff_options = cuffciff_options + ' ' + more_options;

    samples_message = sample_name_1 + "_vs_" + sample_name_2;

    # make the cuffdiff_command
    #cuffdiff [options] <transcripts.gtf> <sample1_replicate1.bam,...> <sample2_replicate1.bam,...> 
    cuffdiff_command = "%s %s -o %s -L %s,%s %s %s %s " % \
        (cuffdiff, cuffdiff_options, output_dir, sample_name_1,sample_name_2,gff_index, sample_1,sample_2);

    # execute the command
    print(cuffdiff_command)
    os.system(cuffdiff_command)

