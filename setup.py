from setuptools import setup

setup(name="sequtil",
      version="0.1b1",
      description="Utilities for processing sequencing data",
      author="Douglas McCloskey",
      author_email="dmccloskey87@gmail.com",
      url="https://github.com/dmccloskey/sequencing_utilities",
      packages=["sequtil"],
      entry_points={"console_scripts":
                    ["makegff = sequencing_utilities.makegff:main",
                     "sam2bam = sequencing_utilities.sam2bam:main",
                     "mapped_percentage = sequencing_utilities.mapped_percentage:main"]}
      )
