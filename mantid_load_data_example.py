# This file runs on the Mantid embedded console
# import mantid algorithms, numpy and matplotlib
from mantid.simpleapi import *
import matplotlib.pyplot as plt
import numpy as np

# import library for managing files
from pathlib import Path
import sys

# a function for reading a list of files from a given directory
def get_files_list(source_dir, file_pattern = '*.nxs'):
    i_counter = 0
    files_list = []
    for filepath in sorted(source_dir.glob(file_pattern)):
        i_counter += 1
        files_list.append(filepath)
    return files_list

files_dir = 'C:/Users/scman1/Desktop/MantisData/TrainingCourseData/'

files_path= Path(files_dir)
files_list = get_files_list(files_path)
print(str(files_list))
for a_file in files_list:
    Load(Filename=str(a_file), OutputWorkspace = a_file.name[:-4])
