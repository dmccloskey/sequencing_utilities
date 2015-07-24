sequencing_utilities
========================
Douglas McCloskey
-----------------

Credits:
-----------------
Ali Ebrahim for writing the original [sequtil](http://github.com/SBRG) library from which this is derived

Installation using Docker:
--------------------------
1. Install [docker](https://docs.docker.com/installation/)

2. at the command terminal, enter "docker pull dmccloskey/sequencing_utilities" to download the docker image from the [dmccloskey](https://hub.docker.com/u/dmccloskey/) dockerhub repo

3. at the command terminal, enter "docker run -i -t --name=sequtils dmccloskey/sequencing_utilities" to bring up an interactive python session in a newly created docker container

Installation from individual packages:
----------------
1.	Install R

2.	Install python and dependencies

3.  Install Bowtie, Bowtie2, Breseq, Samtools, and Cufflinks

Dependencies:
------------
Python 3.4+

[Bowtie](https://github.com/BenLangmead/bowtie)

[Bowtie2](https://github.com/BenLangmead/bowtie2)

[Breseq](https://github.com/barricklab/breseq)

[Samtools](http://samtools.sourceforge.net/)

[Cufflinks](http://cole-trapnell-lab.github.io/cufflinks/announcements/cufflinks-github/)

R 3.01+

Python-dependencies:
-------------------
pysam

numpy

scipy

rpy2

...

(see Dockerfile for a complete list of all packages and dependencies)