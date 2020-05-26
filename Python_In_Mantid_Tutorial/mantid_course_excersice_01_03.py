# import mantid algorithms, numpy and matplotlib
from mantid.simpleapi import *
import matplotlib.pyplot as plt
import numpy as np

# from https://www.mantidproject.org/Python_Exercise_One

# Using ILL Data

# 1    Load - Load the given IN6 data sets, '164198.nxs', '164199.nxs' and '164200.nxs' into workspaces named 
#      after the filename.
#files = ['164198.nxs', '164199.nxs', '164200.nxs']
#for file in files:
#    Load(Filename=file, OutputWorkspace=file[:-4])

# 2    MergeRuns - Merge all the previously loaded data sets into a single workspaced called 'data_merged'.
#merged_data = MergeRuns(InputWorkspaces = "164198, 164199, 164200")
# 3    MaskDetectors - Remove bad spectra indices : 1,2,3,4,5,6,11,14,30,69,90,93,95,97,175,184,190,215,216,217,251,252,253,255,289,317,335 and 337.
MaskDetectors(merged_data, SpectraList= [1,2,3,4,5,6,11,14,30,69,90,93,95,97,175,184,190,215,216,217,251,252,253,255,289,317,335,337])
# check that spectrum 1 is masked
# sample code from mantid help at:
#     https://docs.mantidproject.org/nightly/algorithms/MaskDetectors-v1.html?highlight=maskdetectors
spec = merged_data.getSpectrum(1)
detid = spec.getDetectorIDs()[0]
print('Spectrum number is {}'.format(spec.getSpectrumNo()))
print('Detector of this spectrum is masked: {}'.format(merged_data.getInstrument().getDetector(detid).isMasked()))
# 4    MultiplyRange - Calculate sample transmission of 95%.

# 5    ConvertUnits - Convert the data from TOF to Delta Energy.
# 6    DetectorEfficiencyCorUser - Calculate the detector efficiency for this instrument.
