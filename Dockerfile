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

# File Author / Maintainer
MAINTAINER Douglas McCloskey <dmccloskey87@gmail.com>

# Install git
RUN apt-get update && apt-get install -y git

# Install sequtils from github
WORKDIR /user/local/
RUN git clone https://github.com/dmccloskey/sequencing_utilities

# add sequtils to path
ENV PATH /user/local/sequencing_utilities:$PATH

# Cleanup
RUN rm -rf /tmp
RUN apt-get clean
