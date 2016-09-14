#!/usr/bin/env python
import os
import csv, sys, json

def run_cuffnorm_docker(samples_host_dirs,samples_names,
                    organism_I,host_indexes_dir_I,host_dirname_O, threads = 1,
                   library_norm_method = 'geometric', 
                   library_type ='fr-firststrand',
                    index_type_I = '.gtf',
                   more_options=None):
    '''Process RNA sequencing data
    INPUT:
    samples_host_dirs = list of sample directories for each replicate in sample 1-N
        use "," to seperate replicates per sample
        use "|" to seperate lists of replicates
        s1-r1,s1-r2,s1-r3,...|s2-r1,s2-r2,s2-r3,...|...|sN-r1,sN-r2,sN-r3,...
    samples_names = sample name for sample 1-N
        s1,s2,...,sN,...
    organism_I = name of index
    host_indexes_dir_I = directory for indexes
    host_dirname_O = location for output on the host

    EXAMPLE:
    samples_names = 140818_11_OxicEvo04EcoliGlcM9_Broth-4
    samples_host_dirs = /media/proline/dmccloskey/Resequencing_RNA/fastq/140818_11_OxicEvo04EcoliGlcM9_Broth-4/140818_11_OxicEvo04EcoliGlcM9_Broth-4.bam (remote storage location)
    organism_I = e_coli
    host_indexes_dir_I = /media/proline/dmccloskey/Resequencing_RNA/indexes/ (remote storage location)
    host_dirname_O = /media/proline/dmccloskey/Resequencing_RNA/fastq/ (remote storage location)
    '''
    #1. create a container named rnaseq using sequencing utilities
    #2. mount the host file
    #3. run docker
    docker_mount_1 = '/media/Sequencing/fastq/'
    docker_mount_2 = '/media/Sequencing/indexes/'

    samples_message = samples_names.split(",")[0] + "_to_" + samples_names.split(",")[-1] + "_cuffnorm";

    user_output = '/home/user/'+samples_message;
    container_name = 'cuffnorm';
    
    # make the samples mount for the container
    samples_mount = "";
    docker_name_dir_1 = [];
    for sample_replicates in samples_host_dirs.split('|'):
        docker_name_dir_tmp = [];
        for sample in sample_replicates.split(','):
            filename = sample.split('/')[-1];
            samples_mount += "-v " + sample + ":" + docker_mount_1 + filename + " ";
            docker_name_dir_tmp.append(docker_mount_1 + sample.split('/')[-1])
        docker_name_dir_1.append(','.join(docker_name_dir_tmp))
    samples_mount = samples_mount[:-1];
    docker_name_dir_1_str = '|'.join(docker_name_dir_1);

    if not more_options:
        more_options = 'None';

    rnaseq_cmd = ("run_cuffnorm('%s','%s','%s','%s',indexes_dir='%s',threads=%s,library_norm_method='%s',library_type='%s',index_type='%s',more_options=%s);" \
        %(docker_name_dir_1_str,samples_names,\
        organism_I,user_output,docker_mount_2,\
        threads,library_norm_method,library_type,index_type_I,more_options));
    python_cmd = ("from sequencing_utilities.cuffdiff import run_cuffnorm;%s" %(rnaseq_cmd));
    docker_run = ('docker run -u=root --name=%s %s -v %s:%s dmccloskey/sequencing_utilities python3 -c "%s"' \
        %(container_name,samples_mount,host_indexes_dir_I,docker_mount_2,python_cmd));
    os.system("echo %s" %(docker_run));
    os.system(docker_run);
    #copy the output directory file out of the docker container into the host dir
    docker_cp = ("docker cp %s:%s/ %s/%s" %(container_name,user_output,host_dirname_O,samples_message));
    os.system(docker_cp)
    #delete the container and the container content:
    cmd = ('docker rm -v %s' %(container_name));
    os.system(cmd);
    
def run_cuffnorm_docker_fromCsvOrFile(filename_csv_I = None,filename_list_I = []):
    '''Call run_cuffnorm_docker on a list of parameters
    INPUT:
    filename_list_I = [{sample_name_1:...,sample_name_2:...,},...]
    '''
    if filename_csv_I:
        filename_list_I = read_csv(filename_csv_I);
    for row_cnt,row in enumerate(filename_list_I):
        cmd = ("echo running cuffnorm for samples %s" %(row['samples_names']));
        os.system(cmd);
        run_cuffnorm_docker(row['samples_host_dirs'],
                            row['samples_names'],
                            row['organism_I'],row['host_indexes_dir_I'],
                            row['host_dirname_O'],
                            row['threads'],row['library_norm_method'],
                            row['library_type'],
                          row['index_type_I'],
                            row['more_options']);
         
def read_csv(filename):
    """read table data from csv file"""
    data_O = [];
    try:
        with open(filename, 'r') as csvfile:
            reader = csv.DictReader(csvfile);
            try:
                keys = reader.fieldnames;
                for row in reader:
                    data_O.append(row);
            except csv.Error as e:
                sys.exit('file %s, line %d: %s' % (filename, reader.line_num, e));
    except IOError as e:
        sys.exit('%s does not exist' % e);
    return data_O;

def main_singleFile():
    """Run cuffnorm using docker
    e.g. python3 run_cuffnorm_docker.py ...
    """
    from argparse import ArgumentParser
    parser = ArgumentParser("process RNAseq data")
    parser.add_argument("samples_host_dirs", help="""list of .bam files for samples""")
    parser.add_argument("samples_names", help="""sample names for samples""")
    parser.add_argument("organism_I", help="""name of index""")
    parser.add_argument("host_indexes_dir_I", help="""directory for indexes""")
    parser.add_argument("host_dirname_O", help="""location for output on the host""")
    parser.add_argument("threads", help="""number of processors to use""")
    parser.add_argument("library_norm_method", help="""method for library normalization""")
    parser.add_argument("library_type", help="""the type of library used""")
    parser.add_argument("index_type_I", help="""index file type (.gtf or .gff)""")
    parser.add_argument("more_options", help="""string representation of additional cuffnorm options""")
    args = parser.parse_args()
    run_cuffnorm_docker(args.samples_host_dirs,
                      args.samples_names,
                      args.organism_I,args.host_indexes_dir_I,
                      args.host_dirname_O,
                      args.threads,args.library_norm_method,
                      args.fdr,args.library_type,args.more_options);

def main_batchFile():
    """process RNAseq data using docker in batch
    e.g. python3 run_cuffnorm_docker.py '/media/proline/dmccloskey/Resequencing_RNA/cuffnorm_files.csv' []
    """
    from argparse import ArgumentParser
    parser = ArgumentParser("process RNAseq data")
    parser.add_argument("filename_csv_I", help="""list of files and parameters in a .csv""")
    parser.add_argument("filename_list_I", help="""list of files and parameters e.g. [{sample_name_1:...,sample_name_2:...,},...]""")
    args = parser.parse_args()
    run_cuffnorm_docker_fromCsvOrFile(args.filename_csv_I,args.filename_list_I);

if __name__ == "__main__":
    #main_singleFile();
    main_batchFile();