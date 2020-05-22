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
filename = os.environ['USERPROFILE'] + '\Desktop\MantisData\TrainingCourseData' + r"\PG3_4871_event.nxs"
filename = os.environ['USERPROFILE'] + '\Desktop\MantisData\TrainingCourseData' + r"\LogWS.nxs"
filename = os.environ['USERPROFILE'] + '\Desktop\MantisData\TrainingCourseData' + r"\MUSR00015189_cropped.nxs"


# in mantid 2D workspaces, the plottable data is in the group called workspace
data_groups = ['workspace']

with h5py.File(filename, "r") as nx:
    print(f"file: {nx.filename}")
    
    nx_tree = get_tree(nx)
    # the first group is the root of the nexus file
    root = list(nx_tree.keys())[0]
    # Mantid workspace2D stores data in workspace root child element
    # look if the groups below root contain workspace
    if "workspace" in nx_tree[root][0].keys():
        print (nx_tree[root][0]['workspace'][0])
        print (len(nx_tree[root][0]['workspace'][0]), "elements in workspace group")
        values_path = nx_tree[root][0]['workspace'][0]['values'][0]
        axis1_path = nx_tree[root][0]['workspace'][0]['axis1'][0]
        axis2_path = nx_tree[root][0]['workspace'][0]['axis2'][0]
        errors_path = nx_tree[root][0]['workspace'][0]['errors'][0]
        y_vals = nx[values_path][()][0] # plottable values
        a1_vals = nx[axis1_path][()] # bucket markers
        a2_vals = nx[axis2_path][()]
        er_vals = nx[errors_path][()] # error values
        # get the middle of buckets
        lower = a1_vals[()][:-1]
        upper = a1_vals[()][1:]
        mid_b = lower + (upper - lower)/2
        print ("y vals:", y_vals, "\nmid bin:", mid_b, "\na2:", a2_vals,"\nerrors:", er_vals)
        # plot(x,y, label)
        plt.plot(mid_b, y_vals, label='signal')
        plt.xlabel('x')
        plt.ylabel('counts')
        plt.legend() # include the leyend in the plot
        plt.grid(color='r', linestyle=':', linewidth=1) #show and format grid
        plt.title(nx.filename)
        plt.show()
