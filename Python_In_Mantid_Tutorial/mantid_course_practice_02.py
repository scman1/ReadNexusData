# import mantid algorithms, numpy and matplotlib
from mantid.simpleapi import *
import matplotlib.pyplot as plt
import numpy as np

# from https://www.mantidproject.org/Workspace_Types_Via_Python

ws = Load(Filename="GEM38370_Focussed.nxs", OutputWorkspace="myWS")
print(ws.getComment())
print(ws.getMemorySize())
print(ws.getName())
print(ws.getTitle())
print(ws)