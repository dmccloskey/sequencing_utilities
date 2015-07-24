sequencing_utilities
========================
Douglas McCloskey
-----------------

Credits:
-----------------
Ali Ebrahim for writing the original [sequtil](http://github.com/SBRG) library from which this is derived

Installation using Docker:
--------------------------
1. Install docker

2. enter "docker pull dmccloskey/sequencing_utilities" to download the docker image

3. run "docker -i -t dmccloskey/sequencing_utilties" to bring up an interactive python session

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