# Read Nexus Data
Use python to read data from nexus files

Nexus is the file type used for storing experiments data both at ISIS and Diamond, so it is useful to know how to read these datasets. 
The underlying storage format is HDF5, so the h5py library can be used directly to open and read the data in nexus (.nxs) files
