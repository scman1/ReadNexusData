# import mantid algorithms, numpy and matplotlib
from mantid.simpleapi import *
import matplotlib.pyplot as plt
import numpy as np

# from https://www.mantidproject.org/Python_MatrixWorkspace_v2
ws2D = Load(Filename="LOQ49886.nxs")

# Basic queries 
print("Number of histograms: " + str(ws2D.getNumberHistograms()))
print("Is histogram data: " + str(ws2D.isHistogramData()))
print("Number of bins: " + str(ws2D.blocksize()))

# More advanced queries 
spectrumAxis = ws2D.getAxis(1)
print("Is spectra axis: " + str(spectrumAxis.isSpectra()))
print("Number of spectra: " + str(spectrumAxis.length()))

xAxis = ws2D.getAxis(0)
xUnit = xAxis.getUnit()
print("X-Unit: "  + str(xUnit.unitID() + ', ' + xUnit.caption() + ', ' + str(xUnit.symbol())))

# Get x-axis data as a NumPy array
xData = ws2D.readX(9683)
print("X-Data type: " + str(type(xData)))
print("X-Data:")
print(xData)

# Get y-axis data and error data
print("Y-Data:")
print(ws2D.readY(9683))
print("E-Data:")
print(ws2D.readE(9683))

# Looping over each spectrum and obtaining a read-only reference to the counts
for i in range(ws2D.getNumberHistograms()):
	counts = ws2D.readY(i)
    
print ("counts", counts)

eventWS = Load(Filename="CNCS_7860_event.nxs")
print ("Type of Workspace: ", eventWS.id())
print  ("EventWorkspace called %s contains %s events" %(eventWS.name(), eventWS.getNumberEvents()))