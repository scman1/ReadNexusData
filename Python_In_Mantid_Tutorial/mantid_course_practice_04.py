# import mantid algorithms, numpy and matplotlib
from mantid.simpleapi import *
import matplotlib.pyplot as plt
import numpy as np

# from: https://www.mantidproject.org/Python_ITableWorkspace_v2
table = CreateEmptyTableWorkspace()
table.addColumn("double", "x")
table.addColumn("double", "y")
table.addRow([1.0, 3.0])

# Returns a dictionary of values with column names as keys
print(table.row(0))
# Returns all the data in the table from the specified column as a list
print(table.column("y"))
# Returns just the entry at the specified row and column
print(table.cell(0,0))
