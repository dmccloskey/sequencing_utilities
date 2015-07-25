#!/bin/sh

#
# Downloads the sequence for a strain of e. coli from NCBI and builds a
# Bowtie index for it
#

GENOMES_MIRROR=ftp://ftp.ncbi.nlm.nih.gov/genomes

BOWTIE_BUILD_EXE=bowtie2-build

CUFFLINKS_GFFREAD_EXE=gffread

# build the bowtie index
if [ ! -x "$BOWTIE_BUILD_EXE" ] ; then
	if ! which bowtie2-build ; then
		echo "Could not find bowtie2-build in current directory or in PATH"
		exit 1
	else
		BOWTIE_BUILD_EXE=`which bowtie2-build`
	fi
fi

if [ ! -f NC_000913.fna ] ; then
	if ! which wget > /dev/null ; then
		echo wget not found, looking for curl...
		if ! which curl > /dev/null ; then
			echo curl not found either, aborting...
		else
			# Use curl
			curl ${GENOMES_MIRROR}/Bacteria/Escherichia_coli_K_12_substr__MG1655_uid57779/NC_000913.fna -o NC_000913.fna
		fi
	else
		# Use wget
		wget ${GENOMES_MIRROR}/Bacteria/Escherichia_coli_K_12_substr__MG1655_uid57779/NC_000913.fna
	fi
fi

if [ ! -f NC_000913.fna ] ; then
	echo "Could not find NC_000913.fna file!"
	exit 2
fi

echo Running ${BOWTIE_BUILD_EXE} NC_000913.fna e_coli
${BOWTIE_BUILD_EXE} NC_000913.fna e_coli
if [ "$?" = "0" ] ; then
	echo "e_coli index built:"
	echo "You may remove NC_000913.fna"
else
	echo "Index building failed; see error message"
fi

# generate the .gtf file for cufflinks
if [ ! -x "$CUFFLINKS_GFFREAD_EXE" ] ; then
	if ! which bowtie-build ; then
		echo "Could not find gffread in current directory or in PATH"
		exit 1
	else
		BOWTIE_BUILD_EXE=`which gffread`
	fi
fi

if [ ! -f NC_000913.gff ] ; then
	if ! which wget > /dev/null ; then
		echo wget not found, looking for curl...
		if ! which curl > /dev/null ; then
			echo curl not found either, aborting...
		else
			# Use curl
			curl ${GENOMES_MIRROR}/Bacteria/Escherichia_coli_K_12_substr__MG1655_uid57779/NC_000913.gff -o NC_000913.gff
		fi
	else
		# Use wget
		wget ${GENOMES_MIRROR}/Bacteria/Escherichia_coli_K_12_substr__MG1655_uid57779/NC_000913.gff
	fi
fi

if [ ! -f NC_000913.gff ] ; then
	echo "Could not find NC_000913.gff file!"
	exit 2
fi
 
echo Running ${CUFFLINKS_GFFREAD_EXE} -E NC_000913.gff -T -o e_coli.gtf
${CUFFLINKS_GFFREAD_EXE} -E NC_000913.gff -T -o e_coli.gtf
if [ "$?" = "0" ] ; then
	echo "e_coli .gtf built:"
	echo "   e_coli.gtf"
	echo "You may remove NC_000913.gff"
else
	echo "Conversion failed; see error message"
fi
#echo Running mv NC_000913.gff e_coli.gff 
#mv NC_000913.gff e_coli.gff

