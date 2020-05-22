# import mantid algorithms, numpy and matplotlib
from mantid.simpleapi import *
import matplotlib.pyplot as plt
import numpy as np

# from https://www.mantidproject.org/Running_Algorithms_With_Python

# This example just has .RAW extension but it is able to load all 
# file types that Mantid is aware of.
# run = Load('filename.nxs')
run = Load('HRP39182.RAW')
# ommited arguments will fallback to default values provided in the 
# algorithm definition
run = ConvertUnits(InputWorkspace=run, Target='dSpacing')

# When arguments are provided as pure positional arguments,
# the order in which arguments are given matters and 
# misplacement of arguments can cause errors
run = ConvertUnits(run, 'dSpacing', 'Direct', 85, False)

# When arguments are provided with keywords, the order in
# arguments are given is not important
run = ConvertUnits(InputWorkspace=run, Target='dSpacing', EMode='Direct', EFixed=85, AlignBins=False)

ws = CreateSampleWorkspace()

# The result variable will contain a tuple: (OutputWorkspace, JoinWavelength)
outWS, wavelength = UnwrapMonitor(InputWorkspace=ws,LRef=11)

print("OutputWorkspace is a: ")
print(type(outWS))
print("JoinWavelength is a: ")
print(type(wavelength))

# Alternatively we can unpack the tuple later
result = UnwrapMonitor(InputWorkspace=ws,LRef=11)

print("OutputWorkspace is a: ")
print(type(result[0]))
print("JoinWavelength is a: ")
print(type(result[1]))

# From Mantid 3.10 named tuples can be used
print("OutputWorkspace is a: ", type(result.OutputWorkspace))
print("JoinWavelength is a: ", type(result.JoinWavelength), "\nvalue:", result.JoinWavelength)

