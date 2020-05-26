# import mantid algorithms, numpy and matplotlib
from mantid.simpleapi import *
import matplotlib.pyplot as plt
import numpy as np

# from https://www.mantidproject.org/Python_Exercise_One

# Using SNS Data

# 1    LoadEventNexus - Load the given POWGEN data set, PG3_4871 into a workspace named 'PG3_4871'. 
#      If you need to reduce the number of events loaded, select only the first 4000 seconds of the run.
run = Load(Filename="PG3_4871_event.nxs", OutputWorkspace="PG3_4871")
# 2    View the number of events in the logging window with the command logger.notice(message) 
#      (The function to get the number of events is 'getNumberEvents()'.
num_events = run.getNumberEvents()
message = "Events in PG3 4871: " + str(num_events)
logger.notice(message)
# 3    FilterBadPulses - Remove events that occurred while the accelerator was resetting. 
#      You can view the logs by right clicking on the workspace and selecting 'Sample logs...'
filtered = FilterBadPulses('PG3_4871', LowerCutoff=99.5)
# 4    AlignDetectors - Convert to d-spacing using the supplied calibration file called PG3_golden.cal
AlignDetectors('filtered', "PG3_golden.cal",OutputWorkspace='aligned')
# 5    Rebin - Bin the data in d-spacing from 1.4 to 8 angstroms using logarithmic binning of .0004.
Rebin('aligned', Params=[1.4,-0.0004, 8],OutputWorkspace='rebined')
# 6    DiffractionFocussing - Focus the data in the workspace using the same cal file as the previous 
#      step (PG3_golden.cal).
DiffractionFocussing('rebined', "PG3_golden.cal", OutputWorkspace='focused')
# 7    CompressEvents - Saves some memory. Note the number of events again.
compressed = CompressEvents(InputWorkspace='focused')
nevents = compressed.getNumberEvents()
logger.notice(str(nevents))