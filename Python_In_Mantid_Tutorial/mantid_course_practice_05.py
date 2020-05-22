# import mantid algorithms, numpy and matplotlib
from mantid.simpleapi import *
import matplotlib.pyplot as plt
import numpy as np

# from https://www.mantidproject.org/Python_WorkspaceGroup_v2

Load(Filename="MUSR00015189", OutputWorkspace="groupWS")
groupWS = mtd["groupWS"]
print("Workspace Type: " + groupWS.id())

# The following for loops return the same result

for i in range(groupWS.size()):
	print(groupWS[i].name())
    
for ws in groupWS:
	print(ws.name())
    
print("Is multi-period data: {}".format(str(groupWS.isMultiPeriod())))   