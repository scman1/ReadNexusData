# import mantid algorithms, numpy and matplotlib
from mantid.simpleapi import *
import matplotlib.pyplot as plt
import numpy as np

# from https://www.mantidproject.org/Python_Exercise_One

# Using ISIS Data
# Removing the HRPD Prompt Pulse

# 1. Load the given HRPD data set, HRP39182.RAW into a workspace called 'HRP39182'
Load(Filename="HRP39182.RAW", OutputWorkspace="HRP39182")

# help(MaskBins)
# MaskBins(InputWorkspace, XMin, XMax, InputWorkspaceIndexType=None, InputWorkspaceIndexSet=None, SpectraList=None)
#    Marks bins in a workspace as being masked.

# Mask out the bins corresponding to the pulse with XMin=19990 and XMax=20040 and an output 
# workspace called 'masked'
MaskBins("HRP39182", 19990, 20040,  OutputWorkspace='masked')

# Repeat the previous step for the other 4 pulses, each of which is 20000 microseconds after 
# the previous. 
# All MaskBins executions should happen on the same InputWorkspace so that all 5 pulses are 
# masked from the same workspace.


indx_i = 0
while indx_i < 5:
    min_x = 10990 + (indx_i*20000)
    max_x = 20040 + (indx_i*20000)
    MaskBins("HRP39182", min_x, max_x,  OutputWorkspace='masked')
    indx_i +=1
    
# Correct the masked workspace for small variations in detector position, using the calibration
# file "hrpd_new_072_01_corr.cal". (Note: This performs an explicit conversion to dSpacing) 

# help(AlignDetectors)
# AlignDetectors(InputWorkspace, CalibrationFile=None, CalibrationWorkspace=None, OffsetsWorkspace=None)
#    Performs a unit change from TOF to dSpacing, correcting the X values to account for small errors in 
#    the detector positions.
AlignDetectors('masked', "hrpd_new_072_01_corr.cal",OutputWorkspace='masked')

# help(DiffractionFocussing)
# DiffractionFocussing(InputWorkspace, GroupingFileName=None, GroupingWorkspace=None, PreserveEvents=None)
#    Algorithm to focus powder diffraction data into a number of histograms according to a grouping scheme
#    defined in a CalFile.
DiffractionFocussing('masked', "hrpd_new_072_01_corr.cal", OutputWorkspace='masked')