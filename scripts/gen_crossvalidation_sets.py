# divide a dataset into cross validation groups
#
import os
import common as cmn
import re
import itertools as it
import numpy as np
import errno

# function for parsing filename
def parse_filename(fn_str, pattern):
    p = re.compile(pattern)
    m = p.search(fn_str)
    class_ix = m.group(1)
    instance_ix = m.group(2)
    return (class_ix, instance_ix)

def yield_first(lst, i):
    for tpl in lst:
        if tpl[0] == i: return tpl

def mksymlink(class_ix, instance, group_ix, phase):
    fn_str = 'obj' + str(class_ix) + '__' + str(instance) + '.png'
    #src_str = src_path_str + '/' + fn_str

    src_str = os.path.join(os.path.realpath(src_path_str), fn_str)
    dst_str = dest_path_str + '/' + dirname + str(group_ix) + '/' + phase + '/' + fn_str
    print src_str
    print dst_str
    try:
        os.symlink(src_str, dst_str)
    except OSError, e:
        if e.errno == errno.EEXIST:
            os.remove(dst_str)
            os.symlink(src_str, dst_str)
        else:
            raise e
# read directory of files

phase_dirs = ['train', 'test']
dirname = 'crossval_group_'
fname_patten = "obj([0-9]+)__([0-9]+)\.png" # coil pattern
src_path_str = "../../pics/coil-100/thumbs"
dest_path_str = "../../pics/coil-100"
file_list = os.listdir(src_path_str)
class_dict = {}
# divide into classes
for fname in file_list:
    class_ix, instance_ix = parse_filename(fname, fname_patten)
    if class_ix in class_dict.keys():
        class_dict[class_ix].append(instance_ix)
    else:
        class_dict[class_ix] = [instance_ix]
# split into n groups of train and test partitions
partitions = 3
trainsize = 2
testsize = 1-trainsize
permut_lst = list(it.permutations(np.linspace(0, partitions-1, partitions).astype(int)))
permut_lst = [yield_first(permut_lst, i) for i in range(partitions)]
partition_dict = {}
partition_lst = []

# create directories "crossval_group_n/train", "crossval_group_n/test"
for group_ix in xrange(1, len(permut_lst)+1):
    path_str = dest_path_str + '/' + dirname + str(group_ix)
    if not os.path.exists(path_str):
        os.mkdir(path_str)
    for phase in phase_dirs:
        path_str = dest_path_str + '/' + dirname + str(group_ix) + '/' + phase
        if not os.path.exists(path_str):
            os.mkdir(path_str)

    # copy files to destination
    for class_ix, instances in class_dict.iteritems():
        # divide instances for a class into chunks
        chunks = cmn.chunks_num(instances, partitions)
        for instance in chunks[permut_lst[group_ix-1][0]]:
            mksymlink(class_ix, instance, group_ix, 'test')

        tmp = []
        for x in xrange(1, trainsize+1):
            tmp.extend(chunks[permut_lst[group_ix-1][x]])
        for instance in tmp:
            mksymlink(class_ix, instance, group_ix,  'train')

        