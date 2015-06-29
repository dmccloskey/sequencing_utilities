#!/usr/bin/env python
# PYTHON_ARGCOMPLETE_OK
from os.path import split
from math import log
from warnings import warn

from numpy import zeros, roll

import pysam


def count_coverage(samfile, flip=False, include_insert=False):
    """counts coverage per base in a strand-specific manner

    include_insert: If the insert between paired end reads should be
        included in the counts.

    flip: Whether or not the strands should be flipped.
    This should be true for RNA-seq, and false for ChIP-exo
"""

    all_counts = {}
    plus_strands = []
    minus_strands = []
    chromosome_sizes = dict(list(zip(samfile.references, samfile.lengths)))
    for i in chromosome_sizes:
        chromosome_sizes[i] += 2  # allows to roll later, extra 0's never hurt
    for reference in samfile.references:  # create an array for each reference
        plus_strands.append(zeros((chromosome_sizes[reference],)))
        minus_strands.append(zeros((chromosome_sizes[reference],)))
    # iterate through each mapped read
    for i, read in enumerate(samfile):
        if read.is_unmapped:
            continue
        # for paired and data get entire insert only from read 1
        if include_insert and read.is_proper_pair:
            if read.is_read2:
                continue  # will get handled with read 1
            if read.is_reverse:
                minus_strands[read.tid][read.pnext:read.aend] += 1
            else:
                plus_strands[read.tid][read.pos:read.pos + read.isize] += 1
        else:
            # Truth table for where reads are mapped
            # read2 is flipped

            # is_read1  is_reverse      outcome
            # ---------------------------------
            # True      False           +
            # True      True            -
            # False     False           -
            # False     True            +

            # therefore read1 == is_reverse --> negative
            #           read1 != is_reverse --> positive

            # If unpaired, read.is_read1 will be False,
            # so we need a separate variable.
            is_read1 = not read.is_paired or read.is_read1
            if read.is_reverse == is_read1:
                minus_strands[read.tid][read.pos:read.aend] += 1
            else:
                plus_strands[read.tid][read.pos:read.aend] += 1
    # store the results per reference
    for i, reference in enumerate(samfile.references):
        all_counts[reference] = {}
        # roll shifts by 1, so the first base position (at index 0) is now at
        # index 1
        if flip:
            all_counts[reference]["-"] = roll(plus_strands[i], 1)
            all_counts[reference]["+"] = roll(minus_strands[i], 1)
        else:
            all_counts[reference]["+"] = roll(plus_strands[i], 1)
            all_counts[reference]["-"] = roll(minus_strands[i], 1)
    return all_counts


def count_coverage_5prime(samfile, flip=False):
    """counts the coverage of 5' ends per base in a strand-specific manner

    On paired end reads, this will ignore read 2

    flip: Whether or not the strands should be flipped.
    This should be true for RNA-seq, and false for ChIP-exo
"""

    all_counts = {}
    plus_strands = []
    minus_strands = []
    chromosome_sizes = dict(list(zip(samfile.references, samfile.lengths)))
    for i in chromosome_sizes:
        chromosome_sizes[i] += 2  # allows to roll later, extra 0's never hurt
    for reference in samfile.references:  # create an array for each reference
        plus_strands.append(zeros((chromosome_sizes[reference],)))
        minus_strands.append(zeros((chromosome_sizes[reference],)))
    # iterate through each mapped read
    for i, read in enumerate(samfile):
        if read.is_read2:
            warn("5' only data should not have been processed as Paired-end.")
            continue
        if read.is_unmapped:
            continue
        if read.is_reverse:
            minus_strands[read.tid][read.aend - 1] += 1
        else:
            plus_strands[read.tid][read.pos] += 1
    # store the results per reference
    for i, reference in enumerate(samfile.references):
        all_counts[reference] = {}
        # roll shifts by 1, so the first base position (at index 0) is now at
        # index 1
        if flip:
            all_counts[reference]["-"] = roll(plus_strands[i], 1)
            all_counts[reference]["+"] = roll(minus_strands[i], 1)
        else:
            all_counts[reference]["+"] = roll(plus_strands[i], 1)
            all_counts[reference]["-"] = roll(minus_strands[i], 1)
    return all_counts


def write_samfile_to_gff(sam_filename, out_filename, flip=False, log2=False,
        separate_strand=False, include_insert=False, five_prime=False,
        track=None):
    """write samfile object to an output object in a gff format

    flip: Whether or not the strands should be flipped.
    This should be true for RNA-seq, and false for ChIP-exo

    separate_strand: Whether the forward and reverse strands should be made
    into separate tracks (True) or the negative strand should be rendered
    as negative values (False)

    log2: Whether intensities should be reported as log2.
    """
    samfile = pysam.Samfile(sam_filename)
    if five_prime:
        all_counts = count_coverage_5prime(samfile, flip=flip)
    else:
        all_counts = count_coverage(samfile,
            include_insert=include_insert, flip=flip)
    if track is None:
        name = split(samfile.filename)[1]
    else:
        name = track
    gff_base = "%s\t\t%s\t%d\t%d\t%s\t%s\t.\t.\n"
    if log2:
        str_func = lambda x, s: "%.2f" % (log(x, 2) * s)
    else:
        str_func = lambda x, s: "%d" % (x * s)
    output = open(out_filename, "w")
    for reference in all_counts:
        for strand in all_counts[reference]:
            factor = 1 if strand == "+" else -1
            track_name = "%s_(%s)" % (name, strand) if separate_strand else name
            counts = all_counts[reference][strand]
            for i in counts.nonzero()[0]:
                output.write(gff_base % (reference, track_name, i, i,
                                         str_func(counts[i], factor), strand))
    output.close()
    samfile.close()


def main():
    from argparse import ArgumentParser, RawDescriptionHelpFormatter

    from os.path import isfile, isdir, join

    parser = ArgumentParser("convert a samfile to a gff file", description="""
Below are some useage examples:

Using a profile:
RNAseq:   makegff.py --profile=rna alignment.bam
ChIP-exo: makegff.py --profile=exo alignment.bam

Flip the reads
makegff.py --flip alignment.bam""",
    formatter_class=RawDescriptionHelpFormatter)

    # TODO give more examples in help

    files = parser.add_argument_group("input output arguments")
    files.add_argument("sam_filename", help="sam or bam file to convert to gff")
    files.add_argument("out_filename", nargs="?", default=None,
        help="""Name of gff file to be written. If unspecified, this will be
        [the name of the samfile].gff if that file does not exist.""")

    # have various profiles to set settings
    parser.add_argument("--profile", required=False, default=None,
        choices=["rna", "exo"],
        help="""Use predefined settings from an existing profile""")

    # additional display-related arguments which can be added

    display = parser.add_argument_group("display arguments")
    display.add_argument("--log2", required=False, action="store_true",
        help="""Report values as log2.""")
    display.add_argument("--track", required=False, default=None,
        help="""Name for the gff track.""")
    display.add_argument("--same_track", required=False,
        action="store_true", help="""Put the negative strand on the same track
            as the positive track, only with negative numbers. The default is
            for the strands to be on separate tracks.""")

    # settings can also be changed manually
    manual = parser.add_argument_group("manual counting arguments",
    "Manual control of how counting is done. These are can not be used when"
    "\na profile has been specified.")
    manual.add_argument("--flip", required=False, action="store_true",
        help="""Whether or not the strands should be flipped.
        This should be true for RNA-seq, and false for ChIP-exo.""")
    manual.add_argument("--five_prime", required=False, action="store_true",
                        help="Count only the 5' end of each read, "
                        "ignoring read 2.")
    manual.add_argument("--include_insert", required=False,
        action="store_true", help="""Include the insert between paired
            end reads in the gff counts.""")

    # attempted autocomplete, won't be installed on most systems though
    try:
        from argcomplete import autocomplete
        autocomplete(parser)
    except ImportError:
        None

    args = parser.parse_args()

    # prevent manual settings from being used with existing profiles
    if args.profile is not None:
        for i in ["flip", "five_prime", "include_insert"]:
            if getattr(args, i) is True:
                from sys import exit
                print("Effor: %s cannot be specified with a profile" % i)
                exit(1)

    # handle profiles
    if args.profile == "rna":
        args.flip = True
        args.include_insert = True
        args.five_prime = False
    elif args.profile == "exo":
        args.flip = False
        args.include_insert = False
        args.five_prime = True

    # determine out_filename if none was provided
    out_filename = "" if args.out_filename is None else args.out_filename
    if out_filename == "" or isdir(out_filename):
        if args.sam_filename.endswith(".sam") or \
                args.sam_filename.endswith(".bam"):
            new_filename = args.sam_filename[:-3] + "gff"
        else:
            new_filename = args.sam_filename + ".gff"
        out_filename = join(out_filename, new_filename)
        if isfile(out_filename):  # do not want to overwrite existing
            raise IOError("File %s already exists" % out_filename)

    separate_strand = not args.same_track

    write_samfile_to_gff(args.sam_filename, out_filename,
        five_prime=args.five_prime, include_insert=args.include_insert,
        separate_strand=separate_strand, flip=args.flip, log2=args.log2,
        track=args.track)

if __name__ == "__main__":
    main()
