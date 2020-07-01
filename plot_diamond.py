# read nexus file
# from https://manual.nexusformat.org/examples/h5py/

#library for reading nexus HDF5 data files 
import h5py

# ploting library
import matplotlib.pyplot as plt

# library to get base path for current user
import os

# recursively loop on all groups until data is found and print its contents

def look_up_dataset_names(nx_group):
    dataset_names = []
    for group_key in nx_group.keys():
        #stop condition
        if type(nx_group[group_key]) != h5py._hl.group.Group:
            dataset_names.append(nx_group[group_key].name)
        elif type(nx_group[group_key]) == h5py._hl.group.Group:
            dataset_names += look_up_dataset_names(nx_group[group_key])
    return dataset_names

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

# os.environ['USERPROFILE'] retrieves the base path for current user
# in windows: C:/users/current_user/
filename = os.environ['USERPROFILE'] + '\Desktop\DiamondData\examples' + r"\Rh4CO_pr_021.nxs"

# in mantid 2D workspaces, the plottable data is in the group called workspace
data_groups = ['result']

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
            print(f"- Path to {key} group: {nx_tree[root][0]['result'][0][key][0]}")
            group_paths[key] = nx_tree[root][0]['result'][0][key][0]
            group_vals[key] = nx[group_paths[key]][()]
        print(group_paths)
        print(group_vals)
        print(f"Time points: {len(group_vals['time'])}, data readings: {len(group_vals['data'])}")
        print(f"Energy values: {len(group_vals['energy'])}, data values: {len(group_vals['data'][0])}")
        
        for time_stmp, data_ln in zip(group_vals['time'], group_vals['data']):
            print(time_stmp, data_ln)
            plt.plot(group_vals['energy'], data_ln, label=f"Reading at {time_stmp}")

        plt.xlabel('energy') # label for the x axis
        plt.ylabel('mu')     # label for the y axis
        plt.legend() # include the leyend in the plot
        plt.grid(color='r', linestyle=':', linewidth=1) #show and format grid
        plt.title(nx.filename)
        plt.show()

            
        
