"""retrive local user settings"""

from configparser import ConfigParser
import os as __os
from os.path import isfile as __isfile
from sys import modules

self = modules[__name__]

# define various filepaths
sequtil_dir = __os.path.join(__os.path.dirname(__os.path.abspath(__file__)), "")


def which(program):
    """returns path to an executable if it is found in the path"""
    fpath, fname = __os.path.split(program)
    if fpath:
        if __isfile(program) and __os.access(program, __os.X_OK):
            return program
    else:
        paths_to_search = __os.environ["PATH"].split(__os.pathsep)
        paths_to_search.append(sequtil_dir)
        for path in paths_to_search:
            exe_file = __os.path.join(path, program)
            if __isfile(exe_file) and __os.access(exe_file, __os.X_OK):
                return exe_file
    return ""


# overwrite defaults settings with settings from the file
def load_settings_from_file(filepath="settings.ini", relative=True):
    """reload settings from a different settings file
    
    filepath: The path to the settings file to use
    
    relative: If the path is given relative to the default directory"""
    if relative:
        filepath = __os.path.join(sequtil_dir, filepath)
    config = ConfigParser()
    config.add_section("EXECUTABLES")
    config.add_section("DIRECTORIES")
    # read in any the configuration to update the parser
    config.read(filepath)
    
    executable_names = ["bowtie", "bowtie2", "samtools", "cufflinks",
            "cuffdiff"]

    # for each setting, do the following:
    #   1) set the default value if the setting is missing
    #   2) store the value as a default of this module

    for name in executable_names:
        if not config.has_option("EXECUTABLES", name):
            config.set("EXECUTABLES", name, which(name))
        value = config.get("EXECUTABLES", name)
        value = value if len(value) > 0 else None
        setattr(self, name, value)

    if not config.has_option("DIRECTORIES", "indexes"):
        default_value = __os.path.join(sequtil_dir, "..", "sequencing", "indexes", "")
        default_value = __os.path.join(__os.path.abspath(default_value), "")
        config.set("DIRECTORIES", "indexes", default_value)
    setattr(self, "indexes_dir", config.get("DIRECTORIES", "indexes"))
    
    # write the settings back to the file so missing defaults get stored
    with open(filepath, "w") as outfile:
        config.write(outfile)
    

load_settings_from_file()
del ConfigParser, modules
