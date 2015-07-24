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
    organism_I = 
    host_indexes_dir_I
    local_dirname_I = location for temporary output
    host_dirname_O = location for output on the host

    EXAMPLE:
    basename_I = 140818_11_OxicEvo04EcoliGlcM9_Broth-4
    host_dirname_I = /media/proline/dmccloskey/Resequencing_RNA/fastq/140818_11_OxicEvo04EcoliGlcM9_Broth-4/ (remote storage location)
    organism_I = e_coli
    host_indexes_dir_I = /media/proline/dmccloskey/Resequencing_RNA/indexes/ (remote storage location)
    local_dirname_I = /home/douglas/Documents/Resequencing_RNA/output (local host location)
    host_dirname_O = /media/proline/dmccloskey/Resequencing_RNA/fastq/140818_11_OxicEvo04EcoliGlcM9_Broth-4/ (remote storage location)
    '''
    #1. create a container named rnaseq using sequencing utilities
    #2. mount the host file
    #3. run docker
    docker_mount_1 = '/media/Resequencing_RNA/fastq/'
    docker_mount_2 = '/media/Resequencing_RNA/indexes/'
    user_output = '/home/user/Resequencing_RNA/output/'
    container_name = 'rnaseq';

    rnaseq_cmd = ("process_rnaseq('%s','%s','%s','%s','%s',threads=%s,trim3=%s);" %(basename_I, docker_mount_1,user_output,organism_I,docker_mount_2,threads_I,trim3_I));
    python_cmd = ("from sequencing_utilities.rnaseq import process_rnaseq;%s" %(rnaseq_cmd));
    #TODO
    docker_run = ('sudo docker run --name=%s -v %s:%s -v %s:%s dmccloskey/sequencing_utilities %s' %(container_name,host_dirname_I,docker_mount_1,host_indexes_dir_I,docker_mount_2,python_cmd));
    os.system(docker_run);
    #copy the gff file out of the docker container into a guest location
    docker_cp = ("sudo docker cp %s:%s %s" %(container_name,user_output,local_dirname_I));
    os.system(docker_cp);
    #change the permissions of the file
    #local_dirname = local_dirname_I.split('/')[-1];
    cmd = ("sudo chmod -R 666 %s" %(local_dirname_I));
    os.system(cmd);
    #copy the gff and bam file back to the original bam file location:
    cmd = ('sudo mv %s/%s.bam %s' %(local_dirname_I,basename_I,host_dirname_O));
    cmd = ('sudo mv %s/%s.gff %s' %(local_dirname_I,basename_I,host_dirname_O));
    cmd = ('sudo mv %s/%s/ %s' %(local_dirname_I,basename_I,host_dirname_O));
    os.system(cmd);
    #delete the local copy
    cmd = ('sudo rm -rf %s' %(local_dirname_I));
    os.system(cmd);
    #delete the container and the container content:
    cmd = ('sudo docker rm -v %s' %(container_name));
    os.system(cmd);