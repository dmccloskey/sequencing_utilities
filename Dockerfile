# Dockerfile to build Sequencing_utilities container images
# Based on Ubuntu

# Set the base image to Ubuntu
FROM ubuntu:latest

# Add images to base image
FROM dmccloskey/python3scientific

# switch to root for install
USER root

# File Author / Maintainer
MAINTAINER Douglas McCloskey <dmccloskey87@gmail.com>

# Install dependencies and bowtie, bowtie2, and samtools
RUN apt-get update && apt-get install -y wget \
	unzip \
	git \
	build-essential \
	python2.7-dev \
	python-numpy \
	python-matplotlib \
	python-pip
	bowtie \
	bowtie2 \
	samtools

# Install sequencing_utilities from github
WORKDIR /usr/local/
#RUN git clone https://github.com/dmccloskey/sequencing_utilities.git
RUN wget https://github.com/dmccloskey/sequencing_utilities/archive/master.zip
RUN unzip master.zip
RUN mv sequencing_utilities-master sequencing_utilities
WORKDIR /usr/local/sequencing_utilities/
RUN python3 setup.py install
	
# Cleanup
RUN rm -rf /usr/local/sequencing_utilities
RUN rm -rf /usr/local/master.zip

# Install cufflinks from http
WORKDIR /usr/local/
RUN wget http://cole-trapnell-lab.github.io/cufflinks/assets/downloads/cufflinks-2.2.1.Linux_x86_64.tar.gz
RUN tar -zxvf cufflinks-2.2.1.Linux_x86_64.tar.gz

# add cufflinks to path
ENV PATH /usr/local/cufflinks-2.2.1.Linux_x86_64:$PATH

# Cleanup
RUN rm -rf cufflinks-2.2.1.Linux_x86_64.tar.gz

# Install breseq from http
WORKDIR /usr/local/
RUN wget http://github.com/barricklab/breseq/releases/download/v0.26.0/breseq-0.26.0-Linux-x86_64.tar.gz
RUN tar -zxvf breseq-0.26.0-Linux-x86_64.tar.gz

# add breseq to path
ENV PATH /usr/local/breseq-0.26.0-Linux-x86_64/bin:$PATH

# Cleanup
RUN rm -rf breseq-0.26.0-Linux-x86_64.tar.gz

# Install htseq-count from http
WORKDIR /usr/local/
RUN wget --no-check-certificate https://pypi.python.org/packages/source/H/HTSeq/HTSeq-0.6.1p1.tar.gz
RUN tar -zxvf HTSeq-0.6.1p1.tar.gz
WORKDIR HTSeq-0.6.1p1/
RUN python setup.py install
RUN chmod +x scripts/htseq-count
RUN chmod +x scripts/htseq-qa

# Install htseq-count python dependencies using pip
RUN pip install --upgrade pip
RUN pip install --no-cache-dir HTSeq

# add htseq-count to path
ENV PATH /usr/local/HTSeq-0.6.1p1/scripts:$PATH

# Cleanup
RUN rm -rf /usr/local/HTSeq-0.6.1p1.tar.gz

# Final cleanup
RUN apt-get clean

# Return app user
WORKDIR $HOME
USER user

# Start at the console
CMD ["python3"]
