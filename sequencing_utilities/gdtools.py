#!/usr/bin/python
# -*- coding: latin-1 -*-
"""
Implements the GDTools class that annotates and applies mutations to .gd and reference .gbk files
based on the gdtools utility program
"""
import os

class GDTools():
    def apply(self,gbk_filename_I,gd_filename_I,fastaOrGff3_filename_O,output_O='gff3',
              gdtools_I = 'gdtools'):
        '''apply mutational changes found in the gd file to the reference genome
        e.g. gdtools APPLY [ -o output.gff3 -f GFF3 ] -r reference.gbk input.gd
        INPUT:
        fastaOrGff3_filename_O = output filename
        output_O = 'fasta' or 'gff3' (default output: gff3)
        gbk_filename_I = reference genome
        gd_filename_I = gd filename
        gdtools_I = command for gdtools'''
        cmd = ("%s APPLY -o %s -f %s -r %s %s" %(gdtools_I,fastaOrGff3_filename_O,output_O,gbk_filename_I,gd_filename_I));
        print(cmd);
        os.system(cmd);

    def annotate(self,htmlOrGd_filename_O,gbk_filename_I,gd_filenames_I=[],output_O='html',
              gdtools_I = 'gdtools'):
        '''
        e.g. gdtools ANNOTATE [-o annotated.html] -r reference.gbk input.1.gd [input.2.gd ... ]
        INPUT:
        htmlOrGd_filename_O = filename for the .html or .gd file output
        output_O = 'html' or 'gd' (default output: html)
        gbk_filename_I = reference genome
        gd_filenames_I = list of gd files
        gdtools_I = command for gdtools
        OUTPUT:
        html or gd file based on input

        '''
        gd_filename_str = ' '.join(gd_filenames_I);
        if output_O=='html':
            cmd = ("%s ANNOTATE -o %s --html -r %s %s" %(gdtools_I,
                htmlOrGd_filename_O,gbk_filename_I,gd_filename_str));
        else:
            cmd = ("%s ANNOTATE -o %s -r %s %s" %(gdtools_I,
                htmlOrGd_filename_O,gbk_filename_I,gd_filename_str));
            
        print(cmd);
        os.system(cmd);