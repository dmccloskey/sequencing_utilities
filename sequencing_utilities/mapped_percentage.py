#!/usr/bin/env python
import pysam


def calculate_mapped_percentage(filepath, verbose=False):
    unmapped = 0
    mapped = 0
    samfile = pysam.Samfile(filepath)
    for read in samfile:
        if read.is_unmapped:
            unmapped += 1
        else:
            mapped += 1
    samfile.close()
    percentage = mapped * 100. / (mapped + unmapped)
    if verbose:
        print("For file %s: %d reads mapped (%.2f%%)" % \
                (filepath, mapped, percentage))
    return (mapped, unmapped)


def main():
    import sys
    if len(sys.argv) == 1:
        print("no input files given")
    for i in range(len(sys.argv) - 1):
        calculate_mapped_percentage(sys.argv[i + 1], verbose=True)


if __name__ == "__main__":
    main()
