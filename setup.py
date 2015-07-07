#!/usr/bin/env python

from setuptools import setup

setup(name="sequencing_utilities",
    version="0.1.a1",
    description="Utilities for processing sequencing data",
    author="Douglas McCloskey",
    author_email="dmccloskey87@gmail.com",
    url="https://github.com/dmccloskey/sequencing_utilities",
    packages=["sequencing_utilities"],
    #entry_points={"console_scripts":
    #            ["makegff = sequencing_utilities.makegff:main",
    #                "sam2bam = sequencing_utilities.sam2bam:main",
    #                "mapped_percentage = sequencing_utilities.mapped_percentage:main"]},
    #classifiers=[
    #'Development Status :: 5 - Production/Stable',
    #'Environment :: Console',
    #'Intended Audience :: Science/Research',
    #'Operating System :: OS Independent',
    #'Programming Language :: Python :: 3.4',
    #'Programming Language :: Cython',
    #'Programming Language :: Python :: Implementation :: CPython',
    #'Topic :: Scientific/Engineering',
    #'Topic :: Scientific/Engineering :: Bio-Informatics'
    #],
    platforms="GNU/Linux, Mac OS X >= 10.7, Microsoft Windows >= 7",
    )
