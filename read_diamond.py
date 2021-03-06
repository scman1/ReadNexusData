# read nexus file
# from https://manual.nexusformat.org/examples/h5py/
import h5py
import numpy

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

def print_tree(nx_tree, level = 0):
    
    for node in nx_tree:
        if nx_tree[node][1]=='group':
            print("\t"*level, "group: ", node, "elements = ",  len(nx_tree[node][0]))
            print_tree(nx_tree[node][0], level + 1)
        else:
            print('\t'*level, node, "data =",  nx_tree[node][0])

# os.environ['USERPROFILE'] retrieves the base path for current user
# in windows: C:/users/current_user/
filename = os.environ['USERPROFILE'] + '\Desktop\DiamondData\examples' + r"\Rh4CO_pr_021.nxs"

with h5py.File(filename, "r") as nx:
    print(f"file: {nx.filename}")
    signal_found = False
    nx_set_names = look_up_dataset_names(nx)
    for grp in nx_set_names:
        print("***", grp, "***\n", nx[grp][()])

for indx, name in enumerate(nx_set_names):
    print(indx, name)

with h5py.File(filename, "r") as nx:
    nx_tree = get_tree(nx)
    # lookup if the nx file contains workspace group with four elements then it is a workspace2d file
    
print_tree(nx_tree)

# plottable data in mantid workspace2D is stored in workspace root child element

