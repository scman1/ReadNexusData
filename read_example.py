# read nexus file
# from https://manual.nexusformat.org/examples/h5py/
import h5py
import numpy

# recursively loop on all groups until data is found and print its contents

def look_up_dataset_names(nx_group):
    groups=[]
    for group_key in nx_group.keys():
        #stop condition
        if type(nx_group[group_key]) != h5py._hl.group.Group:
            groups.append(nx_group[group_key].name)
        elif type(nx_group[group_key]) == h5py._hl.group.Group:
            groups += look_up_dataset_names(nx_group[group_key])
    return groups

filename = "C:\\Users\\scman1\\Desktop\\MantisData\\TrainingCourseData\\PG3_4871_event.nxs"

# smallest nexus file from training course
filename = "C:\\Users\\scman1\\Desktop\\MantisData\\TrainingCourseData\\LogWS.nxs"

with h5py.File(filename, "r") as nx:
    print(f"file: {nx.filename}")
    signal_found = False
    nx_groups = look_up_dataset_names(nx)
    for grp in nx_groups:
        print("***", grp, "***\n", nx[grp][()])
##    # find the default NXentry group
##    print(dir(nx.attrs))
##    print(nx.attrs.items())
##    print(nx.attrs.keys())
##    nx_entry = nx[nx.attrs.items]
##    # find the default NXdata group
##    nx_data = nx_entry[nx_entry.attrs["default"]]
##    # find the signal field
##    signal = nx_data[nx_data.attrs["signal"]]
##    # find the axes field(s)
##    attr_axes = nx_data.attrs["axes"]
##    if isinstance(attr_axes, (set, tuple, list)):
##        #  but check that attr_axes only describes 1-D data
##        if len(attr_axes) == 1:
##            attr_axes = attr_axes[0]
##        else:
##            raise ValueError(f"expected 1-D data but @axes={attr_axes}")
##    axes = nx_data[attr_axes]
##
##    print(f"file: {nx.filename}")
##    print(f"signal: {signal.name}")
##    print(f"axes: {axes.name}")
##    print(f"{axes.name} {signal.name}")
##    for x, y in zip(axes, signal):
##        print(x, y)
