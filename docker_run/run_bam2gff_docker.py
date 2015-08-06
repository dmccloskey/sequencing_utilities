#!/usr/bin/env python
import os
import csv, sys, json

def run_bam2gff_docker(host_bam_I,local_gff_I,host_gff_O):
    '''Convert .bam file to .gff using sequencing_utilities and docker
    INPUT:
    host_bam_I = filename and location for .bam file
    local_gff_I = filename and location for temporary .gff file
    host_gff_O = filename and location for .gff file

    EXAMPLE:
    host_bam_I = /media/proline/dmccloskey/Resequencing_DNA/Evo04ptsHIcrrEvo04EP/Evo04ptsHIcrrEvo04EP/data/reference.bam (remote storage location)
    guest_gff_I = /home/douglas/Documents/Resequencing_DNA/reference.gff/reference.gff (local host location)
    host_gff_O = /media/proline/dmccloskey/Resequencing_DNA/Evo04ptsHIcrrEvo04EP/Evo04ptsHIcrrEvo04EP/data/reference.gff (remote storage location)
    '''
    #1. create a container named bam2gff using sequencing utilities
    #2. mount the host file
    #3. run docker
    
    docker_mount_1 = '/home/user/reference.bam'
    user_output = '/home/user/reference.gff'
    container_name = 'bam2gff';

    python_cmd = ("from sequencing_utilities.makegff import write_samfile_to_gff;write_samfile_to_gff('%s','%s',separate_strand=False);" %(docker_mount_1,user_output));
    docker_run = ('docker run --name=%s -v %s:%s dmccloskey/sequencing_utilities python3 -c "%s"' %(container_name,docker_mount_1,host_bam_I,python_cmd));
    os.system(docker_run);
    #copy the gff file out of the docker container into a guest location
    docker_cp = ("docker cp %s:%s %s" %(container_name,user_output,local_gff_I));
    os.system(docker_cp);
    #change the permissions of the file
    gff_filename = local_gff_I.split('/')[-1];
    cmd = ("chmod 666 %s" %(local_gff_I));
    os.system(cmd);
    #copy the gff file back to the original bam file location:
    cmd = ('mv %s/%s %s' %(local_gff_I,gff_filename,host_gff_O));
    os.system(cmd);
    #delete the local copy
    cmd = ('rm -rf %s' %(local_gff_I));
    os.system(cmd);
    #delete the container and the container content:
    cmd = ('docker rm -v %s' %(container_name));
    os.system(cmd);

def run_bam2gff_docker_fromCsvOrFile(filename_csv_I = None,filename_list_I = []):
    '''Call run_bam2gff_docker on a list of .bam files
    INPUT:
    filename_list_I = [{host_bam_I:...,local_gff_I:...,host_gff_O:...},...]
    '''
    if filename_csv_I:
        filename_list_I = read_csv(filename_csv_I);
    for row_cnt,row in enumerate(filename_list_I):
        cmd = ("echo converting file %s" %(row['host_bam_I']));
        os.system(cmd);
        run_bam2gff_docker(row['host_bam_I'],row['local_gff_I'],row['host_gff_O']);
         
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

if __name__ == "__main__":
    from argparse import ArgumentParser
    parser = ArgumentParser("process RNAseq data")
    parser.add_argument("filename_csv_I", help="""list of files in a .csv""")
    parser.add_argument("filename_list_I", help="""list of files e.g. [{host_bam_I:...,local_gff_I:...,host_gff_O:...},...]""")
    args = parser.parse_args()
    run_bam2gff_docker_fromCsvOrFile(args.filename_csv_I,args.filename_list_I);
