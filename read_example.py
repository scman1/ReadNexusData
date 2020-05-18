# read nexus file
# from https://manual.nexusformat.org/examples/h5py/
import h5py
import numpy

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
def look_up_tree(nx_group, root = ""):
    dataset_names = []
    for group_key in nx_group.keys():
        #stop condition
        if type(nx_group[group_key]) != h5py._hl.group.Group:
            dataset_names.append(nx_group[group_key].name)
        elif type(nx_group[group_key]) == h5py._hl.group.Group:
            dataset_names += look_up_tree(nx_group[group_key])
    return dataset_names

filename = "C:\\Users\\scman1\\Desktop\\MantisData\\TrainingCourseData\\PG3_4871_event.nxs"

# smallest nexus file from training course
filename = "C:\\Users\\scman1\\Desktop\\MantisData\\TrainingCourseData\\LogWS.nxs"

with h5py.File(filename, "r") as nx:
    print(f"file: {nx.filename}")
    signal_found = False
    nx_set_names = look_up_dataset_names(nx)
    for grp in nx_set_names:
        print("***", grp, "***\n", nx[grp][()])

for indx, name in enumerate(nx_set_names):
    print(indx, name)
