# Read Nexus Data
Use python to read data from nexus files

Nexus is the file type used for storing experiments data both at ISIS and Diamond, so it is useful to know how to read these datasets. 
The underlying storage format is HDF5, so the h5py library can be used directly to open and read the data in nexus (.nxs) files.

These examples try to show:

1. How to read and process data from nexus files directly using python (and Jupyter)
    * Examples for loading and reading data
        - read_example.py (python script)
        - Read Data from Nexus File.ipynb (jupyter notebook)
    * examples for plotting data
        - plot_example.py (python script)
        - Read and Plot Data from Mantid Nexus Files.ipynb (jupyter notebook)
2. How to read and process data inside Mantid using python scripts
    * mantid_load_data_example.py (python script) Reads data from a directory and loads them as data groups in mantid
3. How to read and process XAS data from nexus files directly using python and Larch
   * Read nexus data: read_diamond.py (python script)
   * Read and plot: plot_diamond.py (python script)
   * Read and process XAS: process_diamond.py (python script)

# Acknowledgements and Funding
For more details about the of the motivation for the development of the resources
in this repository see:
[UK Catalysis Hub Core Theme](https://ukcatalysishub.co.uk/core/).

UK Catalysis Hub supports the development of this repository, funded by
EPSRC grants:  EP/R026939/1, EP/R026815/1, EP/R026645/1, EP/R027129/1,
and EP/M013219/1(biocatalysis))
