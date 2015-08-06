#!/usr/bin/env python
import os
import csv, sys, json

def run_rnaseq_docker(basename_I,host_dirname_I,organism_I,host_indexes_dir_I,
                      local_dirname_I,host_dirname_O,
                      threads_I=2,trim3_I=3):
    '''Process RNA sequencing data
    INPUT:
    basename_I = base name of the fastq files
    host_dirname_I = directory for .fastq files
    organism_I = name of index
    host_indexes_dir_I = directory for indexes
    local_dirname_I = location for temporary output
    host_dirname_O = location for output on the host

    EXAMPLE:
    basename_I = 140818_11_OxicEvo04EcoliGlcM9_Broth-4
    host_dirname_I = /media/proline/dmccloskey/Resequencing_RNA/fastq/140818_11_OxicEvo04EcoliGlcM9_Broth-4/ (remote storage location)
    organism_I = e_coli
    host_indexes_dir_I = /media/proline/dmccloskey/Resequencing_RNA/indexes/ (remote storage location)
    local_dirname_I = /home/douglas/Documents/Resequencing_RNA/ (local host location)
    host_dirname_O = /media/proline/dmccloskey/Resequencing_RNA/fastq/140818_11_OxicEvo04EcoliGlcM9_Broth-4/ (remote storage location)
    '''
    #1. create a container named rnaseq using sequencing utilities
    #2. mount the host file
    #3. run docker
    docker_mount_1 = '/media/Resequencing_RNA/fastq/'
    docker_mount_2 = '/media/Resequencing_RNA/indexes/'
    user_output = '/home/user/'
    container_name = 'rnaseq';

    rnaseq_cmd = ("process_rnaseq('%s','%s','%s','%s','%s',threads=%s,trim3=%s);" %(basename_I, docker_mount_1,user_output,organism_I,docker_mount_2,threads_I,trim3_I));
    python_cmd = ("from sequencing_utilities.rnaseq import process_rnaseq;%s" %(rnaseq_cmd));
    docker_run = ('docker run --name=%s -v %s:%s -v %s:%s dmccloskey/sequencing_utilities python3 -c "%s"' %(container_name,host_dirname_I,docker_mount_1,host_indexes_dir_I,docker_mount_2,python_cmd));
    os.system(docker_run);
    #copy the gff file out of the docker container into a guest location
    docker_cp = ("docker cp %s:%s%s.bam %s" %(container_name,user_output,basename_I,local_dirname_I));
    os.system(docker_cp);
    docker_cp = ("docker cp %s:%s%s.gff %s" %(container_name,user_output,basename_I,local_dirname_I));
    os.system(docker_cp);
    docker_cp = ("docker cp %s:%s%s.sam %s" %(container_name,user_output,basename_I,local_dirname_I));
    os.system(docker_cp);
    docker_cp = ("docker cp %s:%s%s/ %s" %(container_name,user_output,basename_I,local_dirname_I));
    os.system(docker_cp);
    #change the permissions of the file
    #local_dirname = local_dirname_I.split('/')[-1];
    cmd = ("chmod -R 666 %s" %(local_dirname_I));
    os.system(cmd);
    #copy the gff and bam file back to the original bam file location:
    cmd = ('mv %s%s.bam %s' %(local_dirname_I,basename_I,host_dirname_O));
    os.system(cmd);
    cmd = ('mv %s%s.gff %s' %(local_dirname_I,basename_I,host_dirname_O));
    os.system(cmd);
    cmd = ('mv %s%s.sam %s' %(local_dirname_I,basename_I,host_dirname_O));
    os.system(cmd);
    cmd = ('mv %s%s/ %s' %(local_dirname_I,basename_I,host_dirname_O));
    os.system(cmd);
    ##delete the local copy
    #cmd = ('rm -rf %s' %(local_dirname_I));
    #os.system(cmd);
    #delete the container and the container content:
    cmd = ('docker rm -v %s' %(container_name));
    os.system(cmd);
    
def run_rnaseq_docker_fromCsvOrFile(filename_csv_I = None,filename_list_I = []):
    '''Call run_rnaseq_docker on a list of basenames and directories
    INPUT:
    filename_list_I = [{basename_I:...,host_dirname_I:...,},...]
    '''
    if filename_csv_I:
        filename_list_I = read_csv(filename_csv_I);
    for row_cnt,row in enumerate(filename_list_I):
        cmd = ("echo running rnaseq for basename %s" %(row['basename_I']));
        os.system(cmd);
        run_rnaseq_docker(row['basename_I'],row['host_dirname_I'],row['organism_I'],row['host_indexes_dir_I'],row['local_dirname_I'],row['host_dirname_O'],row['threads_I'],row['trim3_I']);
         
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
    """process RNAseq data using docker
    e.g. python3 run_rnaseq_docker.py '140818_11_OxicEvo04EcoliGlcM9_Broth-4' '/media/proline/dmccloskey/Resequencing_RNA/fastq/140818_11_OxicEvo04EcoliGlcM9_Broth-4/' 'e_coli' '/media/proline/dmccloskey/Resequencing_RNA/indexes/' '/home/douglas/Documents/Resequencing_RNA/output/' '/media/proline/dmccloskey/Resequencing_RNA/fastq/140818_11_OxicEvo04EcoliGlcM9_Broth-4/' 2 3
    """
    from argparse import ArgumentParser
    parser = ArgumentParser("process RNAseq data")
    parser.add_argument("basename_I", help="""base name of the fastq files""")
    parser.add_argument("host_dirname_I", help="""directory for .fastq files""")
    parser.add_argument("organism_I", help="""name of index""")
    parser.add_argument("host_indexes_dir_I", help="""directory for indexes""")
    parser.add_argument("local_dirname_I", help="""location for temporary output""")
    parser.add_argument("host_dirname_O", help="""location for output on the host""")
    parser.add_argument("threads_I", help="""number of processors to use""")
    parser.add_argument("trim3_I", help="""trim 3 bases off of each end""")
    args = parser.parse_args()
    run_rnaseq_docker(args.basename_I,args.host_dirname_I,args.organism_I,args.host_indexes_dir_I,
                      args.local_dirname_I,args.host_dirname_O,
                      args.threads_I,args.trim3_I);

def main_batchFile():
    """process RNAseq data using docker in batch
    e.g. python3 run_rnaseq_docker.py '/media/proline/dmccloskey/Resequencing_RNA/rnaseq_files.csv' []
    """
    from argparse import ArgumentParser
    parser = ArgumentParser("process RNAseq data")
    parser.add_argument("filename_csv_I", help="""list of files and parameters in a .csv""")
    parser.add_argument("filename_list_I", help="""list of files and parameters e.g. [{basename_I:...,host_dirname_I:...,},...]""")
    args = parser.parse_args()
    run_rnaseq_docker_fromCsvOrFile(args.filename_csv_I,args.filename_list_I);

if __name__ == "__main__":
    #main_singleFile();
    main_batchFile();