﻿#!/usr/bin/env python
import os
import csv, sys, json

def run_cuffdiff_docker(samples_host_dir_1,samples_host_dir_2,samples_name_1,samples_name_2,
                    organism_I,host_indexes_dir_I,
                    host_dirname_O, threads = 1,
                   library_norm_method = 'quartile', fdr = 0.05,
                   library_type ='fr-firststrand',
        index_type_I = '.gtf',
                   more_options=None):
    '''Process RNA sequencing data
    INPUT:
    samples_host_dir_1 = list of sample directories for each replicate in sample 1
    samples_host_dir_2 = list of sample directories for each replicate in sample 2
    samples_name_1 = sample name for sample 1
    samples_name_2 = sample name for sample 2
    organism_I = name of index
    host_indexes_dir_I = directory for indexes
    index_type_I = string for index extention (e.g., '.gtf' or '.gff')
    host_dirname_O = location for output on the host

    EXAMPLE:
    samples_name_1 = 140818_11_OxicEvo04EcoliGlcM9_Broth-4
    samples_name_2 = 140716_0_OxicEvo04pgiEcoliGlcM9_Broth-1
    samples_host_dir_1 = /media/proline/dmccloskey/Resequencing_RNA/fastq/140818_11_OxicEvo04EcoliGlcM9_Broth-4/140818_11_OxicEvo04EcoliGlcM9_Broth-4.bam (remote storage location)
    samples_host_dir_2 = /media/proline/dmccloskey/Resequencing_RNA/fastq/140716_0_OxicEvo04pgiEcoliGlcM9_Broth-1/140716_0_OxicEvo04pgiEcoliGlcM9_Broth-1.bam (remote storage location)
    organism_I = e_coli
    host_indexes_dir_I = /media/proline/dmccloskey/Resequencing_RNA/indexes/ (remote storage location)
    host_dirname_O = /media/proline/dmccloskey/Resequencing_RNA/fastq/ (remote storage location)
    '''
    #1. create a container named rnaseq using sequencing utilities
    #2. mount the host file
    #3. run docker
    docker_mount_1 = '/media/Sequencing/fastq/'
    docker_mount_2 = '/media/Sequencing/indexes/'

    samples_message = samples_name_1 + "_vs_" + samples_name_2;

    user_output = '/home/user/'+samples_message;
    container_name = 'cuffdiff';
    
    # make the samples mount for the container
    samples_mount = "";
    docker_name_dir_1 = [];
    docker_name_dir_2 = [];
    for sample in samples_host_dir_1.split(','):
        filename = sample.split('/')[-1];
        samples_mount += "-v " + sample + ":" + docker_mount_1 + filename + " ";
        docker_name_dir_1.append(docker_mount_1 + sample.split('/')[-1])
    for sample in samples_host_dir_2.split(','):
        filename = sample.split('/')[-1];
        samples_mount += "-v " + sample + ":" + docker_mount_1 + filename + " ";
        docker_name_dir_2.append(docker_mount_1 + sample.split('/')[-1])
    samples_mount = samples_mount[:-1];
    docker_name_dir_1_str = ','.join(docker_name_dir_1)
    docker_name_dir_2_str = ','.join(docker_name_dir_2)
    if not more_options:
        more_options = 'None';

    rnaseq_cmd = ("run_cuffdiff(['%s'],['%s'],'%s','%s','%s','%s',indexes_dir='%s',threads=%s,library_norm_method='%s',fdr=%s,library_type='%s',index_type='%s',more_options=%s);" \
        %(docker_name_dir_1_str,docker_name_dir_2_str,samples_name_1,samples_name_2,\
        organism_I,user_output,docker_mount_2,threads,library_norm_method,fdr,library_type,index_type_I,more_options));
    python_cmd = ("from sequencing_utilities.cuffdiff import run_cuffdiff;%s" %(rnaseq_cmd));
    docker_run = ('docker run -u=root --name=%s %s -v %s:%s dmccloskey/sequencing_utilities python3 -c "%s"' %(container_name,samples_mount,host_indexes_dir_I,docker_mount_2,python_cmd));
    os.system("echo %s" %(docker_run));
    os.system(docker_run);
    #copy the output directory file out of the docker container into the host dir
    docker_cp = ("docker cp %s:%s/ %s/%s" %(container_name,user_output,host_dirname_O,samples_message));
    os.system(docker_cp)
    #delete the container and the container content:
    cmd = ('docker rm -v %s' %(container_name));
    os.system(cmd);
    
def run_cuffdiff_docker_fromCsvOrFile(filename_csv_I = None,filename_list_I = []):
    '''Call run_cuffdiff_docker on a list of parameters
    INPUT:
    filename_list_I = [{sample_name_1:...,sample_name_2:...,},...]
    '''
    if filename_csv_I:
        filename_list_I = read_csv(filename_csv_I);
    for row_cnt,row in enumerate(filename_list_I):
        cmd = ("echo running cuffdiff for samples %s vs. %s" %(row['samples_name_1'],row['samples_name_2']));
        os.system(cmd);
        run_cuffdiff_docker(row['samples_host_dir_1'],row['samples_host_dir_2'],
                            row['samples_name_1'],row['samples_name_2'],
                            row['organism_I'],row['host_indexes_dir_I'],
                            row['host_dirname_O'],
                            row['threads'],row['library_norm_method'],
                            row['fdr'],row['library_type'],
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
    """Run cuffdiff using docker
    e.g. python3 run_cuffdiff_docker.py ...
    """
    from argparse import ArgumentParser
    parser = ArgumentParser("process RNAseq data")
    parser.add_argument("samples_host_dir_1", help="""list of .bam files for samples_1""")
    parser.add_argument("samples_host_dir_2", help="""list of .bam files for samples_2""")
    parser.add_argument("samples_name_1", help="""sample name for samples_1""")
    parser.add_argument("samples_name_2", help="""sample name for samples_2""")
    parser.add_argument("organism_I", help="""name of index""")
    parser.add_argument("host_indexes_dir_I", help="""directory for indexes""")
    parser.add_argument("host_dirname_O", help="""location for output on the host""")
    parser.add_argument("threads", help="""number of processors to use""")
    parser.add_argument("library_norm_method", help="""method for library normalization""")
    parser.add_argument("fdr", help="""false discover rate""")
    parser.add_argument("library_type", help="""the type of library used""")
    parser.add_argument("index_type_I", help="""index file type (.gtf or .gff)""")
    parser.add_argument("more_options", help="""string representation of additional cuffdiff options""")
    args = parser.parse_args()
    run_cuffdiff_docker(args.samples_host_dir_1,args.samples_host_dir_2,
                      args.samples_name_1,args.samples_name_2,
                      args.organism_I,args.host_indexes_dir_I,
                      args.host_dirname_O,
                      args.threads,args.library_norm_method,
                      args.fdr,args.library_type,
                      args.index_type_I,args.more_options);


def main_batchFile():
    """process RNAseq data using docker in batch
    e.g. python3 run_cuffdiff_docker.py '/media/proline/dmccloskey/Resequencing_RNA/cuffdiff_files.csv' []
    """
    from argparse import ArgumentParser
    parser = ArgumentParser("process RNAseq data")
    parser.add_argument("filename_csv_I", help="""list of files and parameters in a .csv""")
    parser.add_argument("filename_list_I", help="""list of files and parameters e.g. [{sample_name_1:...,sample_name_2:...,},...]""")
    args = parser.parse_args()
    run_cuffdiff_docker_fromCsvOrFile(args.filename_csv_I,args.filename_list_I);

if __name__ == "__main__":
    #main_singleFile();
    main_batchFile();