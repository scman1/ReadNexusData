# read nexus file

#library for reading nexus HDF5 data files 
import h5py

# files for processing data
import numpy as np

# ploting library
import matplotlib.pyplot as plt

# library to get base path for current user
import os

# import library for managing files
from pathlib import Path

# import library for managing csv files
import csv

#######################################################################
# LARCH imports
#######################################################################
import larch
# larch-xas processing functions
from larch_plugins.xafs import autobk, xftf
# import the larch.io function for merging groups interpolating if necessary
from larch.io import merge_groups
# import the larch.io libraries for managing athena files
from larch.io import create_athena, read_athena, extract_athenagroup
# create a larch interpreter, (to be passed to some functions)
my_larch = larch.Interpreter()

# writes data to the given file name
def write_csv_data(values, filename):
    fieldnames = []
    for item in values.keys():
        for key in values[item].keys():
            if not key in fieldnames:
                fieldnames.append(key)
    #write back to a new csv file
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for key in values.keys():
            writer.writerow(values[key])

# recursively traverse tree and build tree model
def get_tree(nx_group):
    nx_tree={}
    for group_key in nx_group.keys():
        #stop condition
        if type(nx_group[group_key]) == h5py._hl.dataset.Dataset:
            nx_tree[group_key] = [nx_group[group_key].name, "data"]
        elif type(nx_group[group_key]) == h5py._hl.group.Group:
            nx_tree[group_key] = [get_tree(nx_group[group_key]), "group"]
    return nx_tree

# basic plot of a group
# input:
#   - a larch xas group
#   - the detination dir (where to save)
def basic_plot(xas_group, dest_dir, show_plot = False):
    fig=plt.figure(figsize=(10,8))
    plt.tick_params(axis='both', labelsize=6)
    
    # plot grid of results:
    # mu + bkg
    plt.subplot(2, 2, 1)
    plt.title('$\mu$ and background')
    plt.plot(xas_group.energy, xas_group.bkg, 'r--', label = 'background')
    plt.plot(xas_group.energy, xas_group.mu, label = "$\mu$")
    plt.xlabel('Energy (eV)')
    plt.grid(linestyle=':', linewidth=1)
    plt.legend()

    # normalized XANES
    # find array bounds for normalized mu(E) for [e0 - 25: e0 + 75]
    j0 = np.abs(xas_group.energy-(xas_group.e0 - 25.0)).argmin()
    j1 = np.abs(xas_group.energy-(xas_group.e0 + 75.0)).argmin()

    
    plt.subplot(2, 2, 2)
    plt.title('normalized $\mu$')
    plt.plot(xas_group.energy[j0:j1], xas_group.norm[j0:j1], label="$\mu$ Normalised")
    plt.xlabel('Energy (eV)')
    plt.grid(linestyle=':', linewidth=1)
    plt.legend()
    
    # chi(k)
    plt.subplot(2, 2, 3)
    plt.title(r"$\chi(k)$")
    plt.plot(xas_group.k, xas_group.chi*xas_group.k**2, label= r'$ \chi(k^2)$')
    plt.plot(xas_group.k, xas_group.kwin, 'r--', label= r'$k$ window')
    plt.xlabel(r'$ k (\AA^{-1}) $', fontsize='small')
    plt.ylabel(r'$ k^2 \chi(\AA^{-2}) $', fontsize='small')
    plt.grid(linestyle=':', linewidth=1)
    plt.legend()

    # chi(R)
    plt.subplot(2, 2, 4)
    plt.title(r"$\chi(R)$")
    plt.plot(xas_group.r, xas_group.chir_mag, label = r"$\chi(R)$ magnitude")
    plt.plot(xas_group.r, xas_group.chir_re, 'r--', label = r"$\chi(R)$ re")
    plt.xlabel(r'$ R (\AA) $',fontsize='small')
    plt.ylabel(r'$ \chi(R) (\AA^{-3}) $', fontsize='small')
    plt.grid(linestyle=':', linewidth=1)
    plt.legend()

    
    save_as = dest_dir / (xas_group.label + "_01.jpg")

    if not save_as.parent.exists():
        save_as.parent.mkdir(parents=True)
        
    fig.tight_layout(pad=3.0)
    fig.suptitle(xas_group.label)    
    plt.savefig(str(save_as))
    if show_plot:
        plt.show()
    plt.clf()

# save energy and normalised mu
def save_e_nmu(xafsgroup, save_dir):
    export = {}
    for n_index, value in enumerate(xafsgroup.energy):
        export[n_index] = {'energy':value, 'norm':xafsgroup.norm[n_index]}
    write_csv_data(export, save_dir/(xafsgroup.label+"_EvNm.csv"))


# os.environ['USERPROFILE'] retrieves the base path for current user
# in windows: C:/users/current_user/
################################################################################
# ENTRY DATA
################################################################################
file_path = os.environ['USERPROFILE'] + '\Desktop\DiamondData\examples'
name_pattern = "Rh4CO_pr_021.nxs"
file_dir= Path(file_path)
save_dir = file_dir / 'result' / name_pattern[:-4]
filename = file_path + "\\" + name_pattern #os.environ['USERPROFILE'] + '\Desktop\DiamondData\examples' + r"\Rh4CO_pr_021.nxs"


################################################################################
# Open nexus file and get data to process 
################################################################################
with h5py.File(filename, "r") as nx:
    print(f"file: {nx.filename}")
    
    nx_tree = get_tree(nx)
    # the first group is the root of the nexus file
    root = list(nx_tree.keys())[0]
    # Mantid workspace2D stores data in workspace root child element
    # look if the groups below root contain workspace
    if "result" in nx_tree[root][0].keys():
        print ("Nexus tree", nx_tree[root][0])
        group_paths = {}
        group_vals = {}
        for key in nx_tree[root][0]['result'][0].keys():
        #    print(f"- Path to {key} group: {nx_tree[root][0]['result'][0][key][0]}")
            group_paths[key] = nx_tree[root][0]['result'][0][key][0]
            group_vals[key] = nx[group_paths[key]][()]
        #print(group_paths)
        #print(group_vals)
        print(f"Time points: {len(group_vals['time'])}, data readings: {len(group_vals['data'])}")
        print(f"Energy values: {len(group_vals['energy'])}, data values: {len(group_vals['data'][0])}")
        
        for time_stmp, data_ln in zip(group_vals['time'], group_vals['data']):
        #    print(time_stmp, data_ln)
            plt.plot(group_vals['energy'], data_ln, label=f"Reading at {time_stmp}")

        plt.xlabel('energy') # label for the x axis
        plt.ylabel('mu')     # label for the y axis
        plt.legend() # include the leyend in the plot
        plt.grid(color='r', linestyle=':', linewidth=1) #show and format grid
        plt.title(nx.filename)
        plt.show()
        # process groups of files using larch with defaults:
        #   get mu
        #   get energy
        #   plot groups
        #   merge groups
        #   plot merge
        #   save diagrams
        #   save all as athena project
        groups = []
        for time_stmp, data_ln in zip(group_vals['time'], group_vals['data']):
            new_group = larch.Group()
            new_group.mu = data_ln
            new_group.energy = group_vals['energy']
            # run autobk on the xafsdat Group, including a larch Interpreter....
            # note that this expects 'energy' and 'mu' to be in xafsdat, and will
            # write data for 'k', 'chi', 'kwin', 'e0', ... into xafsdat
            autobk(new_group, rbkg=1.0, kweight=2, _larch=my_larch)

            # Fourier transform to R space, again passing in a Group (here,
            # 'k' and 'chi' are expected, and writitng out 'r', 'chir_mag',
            # and so on
            xftf(new_group, kmin=2, kmax=15, dk=3, kweight=2, _larch=my_larch)

            new_group.label = f"Reading at {time_stmp}"
            
            # add group to list
            groups.append(new_group)

            # plot and save each file in group 
            basic_plot(new_group, save_dir)

            # save energy v normalised mu
            save_e_nmu(new_group, save_dir)
        # merge groups
        merged_group = merge_groups(groups)
        merged_group.label = "merged"
        autobk(merged_group, rbkg=1.0, kweight=2, _larch=my_larch)
        xftf(merged_group, kmin=2, kmax=15, dk=3, kweight=2, _larch=my_larch)
        # plot and save for merge
        basic_plot(merged_group, save_dir)
        # save energy v normalised mu for merge
        save_e_nmu(merged_group, save_dir)

        groups.append(merged_group)

        # save as an athena project

        project_name = save_dir / (name_pattern[:-4] + '.prj')
        athena_project = create_athena(project_name)
        for a_group in groups:
            athena_project.add_group(a_group)
        athena_project.save()
        print("Saved athena project " + str(project_name))
