# Dockerfile to build Sequencing_utilities container images
# Based on Ubuntu

# Set the base image to Ubuntu
FROM ubuntu:latest

# Add images to base image
FROM dmccloskey/bowtie1
FROM dmccloskey/bowtie2
FROM dmccloskey/htseq-count
FROM dmccloskey/breseq
FROM dmccloskey/cufflinks
FROM dmccloskey/samtools
FROM dmccloskey/python3scientific

USER root

# File Author / Maintainer
MAINTAINER Douglas McCloskey <dmccloskey87@gmail.com>

# Install git
RUN apt-get update && apt-get install -y wget \
	unzip
#RUN apt-get update && apt-get install -y git

# Install sequtils from github
WORKDIR /user/local/
#RUN git clone https://github.com/dmccloskey/sequencing_utilities.git
RUN wget https://github.com/dmccloskey/sequencing_utilities/archive/master.zip
RUN unzip master.zip
RUN mv sequencing_utilities-master sequencing_utilities
WORKDIR /user/local/sequencing_utilities/
RUN python3 setup.py install
	
# Create sequencing directory
WORKDIR /home/user/
RUN mkdir Sequencing
WORKDIR /home/user/Sequencing
RUN mkdir fastq #data directory
RUN mkdir indices #indices directory
RUN mkdir scripts #shell scripts directory

# Copy shell scripts
RUN mv /user/local/sequencing_utilities/scripts/make_e_coli.sh /home/user/Sequencing/indices/make_e_coli.sh
RUN mv /user/local/sequencing_utilities/scripts/run_cuffdiff.sh /home/user/Sequencing/scripts/run_cuffdiff.sh
RUN mv /user/local/sequencing_utilities/scripts/run_reseq.sh /home/user/Sequencing/scripts/run_reseq.sh
RUN mv /user/local/sequencing_utilities/scripts/run_rnaseq.sh /home/user/Sequencing/scripts/run_rnaseq.sh

# Cleanup
RUN rm -rf /user/local/sequencing_utilities
RUN apt-get clean

# Return app user
WORKDIR $HOME
USER user
