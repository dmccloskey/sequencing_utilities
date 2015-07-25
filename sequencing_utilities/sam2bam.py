#!/usr/bin/env python
# PYTHON_ARGCOMPLETE_OK

import os
from os import system
from os.path import isfile
from time import time

def convert_samfile(samfile, sort=False, force=False, verbose=True,samtools='samtools',threads=1):
    if not isfile(samfile):
        raise IOError("%s is not a file, skipping" % samfile)
    if not samfile.endswith(".sam"):
        print("%s does not end with .sam, is it a samfile? skipping..." % samfile)
        return
    base_name = samfile[:-4]
    bamfile = base_name + ".bam"
    if isfile(bamfile) and not force:
        raise IOError("%s already exists, use force to overwrite" % bamfile)
    if sort:
        command_strs = []
        # sam to unsorted bam
        command_strs.append("%s view -bS -@ %s -o %s.unsorted.bam" %
                            (samtools, threads, samfile, base_name))
        # unsorted bam to sorted bam
        command_strs.append("%s sort -@ %s %s.unsorted.bam %s" %
                            (samtools, threads, base_name, base_name))
        # creation of index
        command_strs.append("%s index %s" % (samtools, bamfile))
        # removal of unsorted bam
        command_strs.append("rm %s.unsorted.bam" % base_name)
    else:
        command_strs = ["%s view -bS %s -o %s" % (samtools, samfile, bamfile)]
    if verbose:
        print("starting processing on " + samfile)
    start = time()
    for command_str in command_strs:
        if verbose:
            print(command_str)
        system(command_str)
    if verbose:
        print("done (%.2f seconds)" % (time() - start))


def main():
    from argparse import ArgumentParser
    try:
        from argcomplete import autocomplete
    except ImportError:
        autocomplete = None

    parser = ArgumentParser("convert samfiles to bamfiles")
    parser.add_argument("--sort", required=False, action="store_true",
            help="sorts the bamfile.")
    parser.add_argument("--force", required=False, action="store_true",
            help="overwrite existing bam file if necessary.")
    parser.add_argument("samfiles", nargs="+")
    if autocomplete is not None:
        autocomplete(parser)
    args = parser.parse_args()
    for samfile in args.samfiles:
        convert_samfile(samfile, args.sort, args.force)

if __name__ == "__main__":
    main()
