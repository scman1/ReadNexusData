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
def get_tree(nx_group):
    dataset_names = []
    nx_tree = {}
    datasets = {}
    data_groups = {}
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

filename = "C:\\Users\\scman1\\Desktop\\MantisData\\TrainingCourseData\\MUSR00015189_cropped.nxs"

# smallest nexus file from training course
## filename = "C:\\Users\\scman1\\Desktop\\MantisData\\TrainingCourseData\\LogWS.nxs"

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
    
print_tree(nx_tree)



class NX_Tree:
    def __init__(self, label, tree_path, groups=None, data_entries=None):
        self.label = label
        self.tree_path  = tree_path
        self.groups = groups                # will contain a list of groups
        self.data_entries = data_entries    # will contain a list of data entries

    def __str__(self):
        return str(self.label)
    

# recursively traverse tree and build tree model
# using NX_Tree
def build_nx_tree(nx_group, parent = None):
    nx_tree = None
    for group_key in nx_group.keys():        
        if parent == None:
            nx_tree = NX_Tree(group_key,nx_group[group_key].name,[],[])
        #stop condition
        if type(nx_group[group_key]) == h5py._hl.dataset.Dataset:
            nx_entry = NX_Tree(group_key,nx_group[group_key].name)
            nx_tree.data_entries.append(nx_entry)
        elif type(nx_group[group_key]) == h5py._hl.group.Group:
            nx_group = NX_Tree(group_key,nx_group[group_key].name)
            nx_tree.groups.append(build_nx_tree(nx_group[group_key],nx_tree))
    return nx_tree
