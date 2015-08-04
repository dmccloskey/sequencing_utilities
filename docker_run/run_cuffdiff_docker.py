#!/usr/bin/env python
import os
import csv, sys, json

def run_cuffdiff_docker(samples_host_dir_1,samples_host_dir_2,samples_name_1,samples_name_2,
                    organism_I,host_indexes_dir_I,
                    local_dirname_I,host_dirname_O, threads = 1,
                   library_norm_method = 'quartile', fdr = 0.05,
                   library_type ='fr-firststrand',
                   more_options=None):
    '''Process RNA sequencing data
    INPUT:
    samples_host_dir_1 = list of sample directories for each replicate in sample 1
    samples_host_dir_2 = list of sample directories for each replicate in sample 2
    samples_name_1 = sample name for sample 1
    samples_name_2 = sample name for sample 2
    organism_I = name of index
    host_indexes_dir_I = directory for indexes
    local_dirname_I = location for temporary output
    host_dirname_O = location for output on the host

    EXAMPLE:
    samples_name_1 = 140818_11_OxicEvo04EcoliGlcM9_Broth-4
    samples_name_2 = 140716_0_OxicEvo04pgiEcoliGlcM9_Broth-1
    samples_host_dir_1 = /media/proline/dmccloskey/Resequencing_RNA/fastq/140818_11_OxicEvo04EcoliGlcM9_Broth-4/140818_11_OxicEvo04EcoliGlcM9_Broth-4.bam (remote storage location)
    samples_host_dir_2 = /media/proline/dmccloskey/Resequencing_RNA/fastq/140716_0_OxicEvo04pgiEcoliGlcM9_Broth-1/140716_0_OxicEvo04pgiEcoliGlcM9_Broth-1.bam (remote storage location)
    organism_I = e_coli
    host_indexes_dir_I = /media/proline/dmccloskey/Resequencing_RNA/indexes/ (remote storage location)
    local_dirname_I = /home/douglas/Documents/Resequencing_RNA/ (local host location)
    host_dirname_O = /media/proline/dmccloskey/Resequencing_RNA/fastq/ (remote storage location)
    '''
    #1. create a container named rnaseq using sequencing utilities
    #2. mount the host file
    #3. run docker
    docker_mount_1 = '/media/Resequencing_RNA/fastq/'
    docker_mount_2 = '/media/Resequencing_RNA/indexes/'

    samples_message = samples_name_1 + "_vs_" + samples_name_2;

    user_output = '/home/user/' + samples_message;
    container_name = 'cuffdiff';
    
    # make the samples mount for the container
    samples_mount = "";
    docker_name_dir_1 = [];
    docker_name_dir_2 = [];
    for sample in samples_host_dir_1.split(','):
        samples_mount += "-v " + sample + ":" + docker_mount_1 + " ";
        docker_name_dir_1.append(docker_mount_1 + '/' + sample.split('/')[-1])
    for sample in samples_host_dir_2.split(','):
        samples_mount += "-v " + sample + ":" + docker_mount_1 + " ";
        docker_name_dir_2.append(docker_mount_1 + '/' + sample.split('/')[-1])
    samples_mount = samples_mount[:-1];

    rnaseq_cmd = ("run_cuffdiff('%s','%s','%s','%s','%s',threads=%d,library_norm_method=%s,fdr=%f,library_type=%s,more_options=%s);" \
        %(docker_name_dir_1,docker_name_dir_2,samples_name_1,samples_name_2,\
        organism_I,user_output,docker_mount_2,threads,library_norm_method,fdr,library_type,more_options));
    python_cmd = ("from sequencing_utilities.cuffdiff import run_cuffdiff;%s" %(rnaseq_cmd));
    docker_run = ('sudo docker run --name=%s %s -v %s:%s dmccloskey/sequencing_utilities python3 -c "%s"' %(container_name,samples_mount,host_indexes_dir_I,docker_mount_2,python_cmd));
    os.system(docker_run);
    #copy the output directory file out of the docker container into a guest location
    docker_cp = ("sudo docker cp %s:%s/ %s" %(container_name,user_output,local_dirname_I));
    os.system(docker_cp);
    #change the permissions of the file
    #local_dirname = local_dirname_I.split('/')[-1];
    cmd = ("sudo chmod -R 666 %s" %(local_dirname_I));
    os.system(cmd);
    #copy the output directory back to the original bam file location:
    os.system(cmd);
    cmd = ('sudo mv %s%s/ %s' %(local_dirname_I,samples_message,host_dirname_O));
    os.system(cmd);
    ##delete the local copy
    #cmd = ('sudo rm -rf %s' %(local_dirname_I));
    #os.system(cmd);
    #delete the container and the container content:
    cmd = ('sudo docker rm -v %s' %(container_name));
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
                            row['local_dirname_I'],row['host_dirname_O'],
                            row['threads'],row['library_norm_method'],
                            row['fdr'],row['library_type'],row['more_options']);
         
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
    parser.add_argument("local_dirname_I", help="""location for temporary output""")
    parser.add_argument("host_dirname_O", help="""location for output on the host""")
    parser.add_argument("threads", help="""number of processors to use""")
    parser.add_argument("library_norm_method", help="""method for library normalization""")
    parser.add_argument("fdr", help="""false discover rate""")
    parser.add_argument("library_type", help="""the type of library used""")
    parser.add_argument("more_options", help="""string representation of additional cuffdiff options""")
    args = parser.parse_args()
    run_cuffdiff_docker(args.samples_host_dir_1,args.samples_host_dir_2,
                      args.samples_name_1,args.samples_name_2,
                      args.organism_I,args.host_indexes_dir_I,
                      args.local_dirname_I,args.host_dirname_O,
                      args.threads,args.library_norm_method,
                      args.fdr,args.library_type,args.more_options);


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