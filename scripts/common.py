# common stuff
import os
import re
import sys
from itertools import chain, product

def readfile(filename):
   fileobj = open(filename, 'r') # open for reading
   retval = fileobj.read() # read all lines into string
   fileobj.close()
   return retval

def writefile(filename, str):
   if not os.path.exists(os.path.dirname(filename)):
      try:
         os.makedirs(os.path.dirname(filename))
      except OSError as exc: # Guard against race condition
         if exc.errno != errno.EEXIST:
            raise
   fileobj = open(filename, 'w')
   fileobj.write(str)
   fileobj.close()

def chunks_sz(lst, sz):
    """Yield successive n-sized chunks from l."""
    for i in xrange(0, len(lst), sz):
        yield lst[i:i+sz]

def chunks_num(lst, size):
   """Yield n chunks from l. (from stackoverflow)"""
   """   http://stackoverflow.com/a/4119142"""
   input_size = len(lst)
   slice_size = input_size / size
   remain = input_size % size
   result = []
   iterator = iter(lst)
   for i in range(size):
      result.append([])
      for j in range(slice_size):
         result[i].append(iterator.next())
      if remain:
         result[i].append(iterator.next())
         remain -= 1
   return result




def get_str_val(in_str, pattern):
   """ search for a match and get the associated value """
   p = re.compile(pattern + "=" + '"([0-9a-zA-Z\.]+)"')
   m = p.search(in_str)
   return m.group(1)
   

def set_str_val(in_str, pattern, value):
   """ set the value of a tag in a string"""
   p = re.compile( pattern + "=" + '"([0-9]+)"')
   return p.sub(pattern + '="' + value + '"', in_str)

def get_input_tag(inp):
   retval = ""
   if 'CIFAR' in inp:
      retval = 'CIFAR'
   elif 'COIL' in inp:
      retval = 'COIL'
   return retval

def parsefilename(fname, maxlayer):
   """recursively parse filename"""
   # weights/csom/C3_weights_COILC1_alpha=0.0001_C1_rf_size=3_C1_rf_inc=1_C1_som_size=4C2_alpha=0.0001_C2_rf_size=3_C2_rf_inc=1_C2_som_size=4_C3_alpha=0.0001_C3_rf_size=3_C3_rf_inc=1_C3_som_size=4.dat
   keys = ["rf_size", "rf_inc", "som_size"]#[key for key, value in csom_parameter_values.iteritems()]
   layerprefix = ['C'+ str(i) for i in range(1, maxlayer+1)]
   keys = map('_'.join, product(layerprefix, keys))
   retval = {}
      #print "C1_"+key
   for pattern in keys:
      #p = re.compile(pattern + "=" + '([0-9a-zA-Z]+)')
      p = re.compile(pattern + "=" + '([0-9]+)')
      m = p.search(fname)
      val = m.group(1)
      retval.update({pattern:int(val)})
   #print get_str_val(fname, "C1_"+key)
   retval.update({"input":get_input_tag(fname)})
   # add index if exists
   p = re.compile("_" + '([0-9]+)' +'-' + '([0-9]+)'+'\.')
   m = p.search(fname)
   if(m):
      val = m.group(1)
      retval.update({"ix":int(val)})
   return retval

def parsefilename_span(fname, maxlayer):
   """recursively parse filename with support for span"""
   # weights/csom/C1_wghts_C1(rf(3-3)_inc(1-1)_som(12-3)_block(3-3)_span(0-0)).dat
   keys = ["rf", "inc", "som", "span", "block"]#[key for key, value in csom_parameter_values.iteritems()]
   
   layerprefix = ['C'+ str(i) for i in range(1, maxlayer+1)]
   #keys = map('_'.join, product(layerprefix, keys))
   retval = {}
      #print "C1_"+key
   for pattern in layerprefix:
      #p = re.compile(pattern + "=" + '([0-9a-zA-Z]+)')
      p = re.compile(pattern + '\(' + '([\-_a-z0-9\(\)]+)'+'\)?')
      m = p.search(fname)
      val = m.group(1)
      for key in keys:
         # print val
         p = re.compile(key + '\(' + '([0-9]+)' + '-' + '([0-9]+)' + '\)' )
         m = p.search(val)
         x = m.group(1)
         y = m.group(2)

         retval.update({pattern+'_'+key+'_size_x':int(x)})
         retval.update({pattern+'_'+key+'_size_y':int(y)})
   #print get_str_val(fname, "C1_"+key)
   retval.update({"input":get_input_tag(fname)})
   # add index if exists
   p = re.compile("_" + '([0-9]+)' +'-' + '([0-9]+)'+'\.')
   m = p.search(fname)
   if(m):
      val = m.group(1)
      retval.update({"ix":int(val)})
   return retval

def read_ikaros_csv(fname):
   # return dict with the different outputs
   with open(fname, 'r') as fileobj: # open for reading
      first = True
      p = re.compile('([A-Za-z0-9]+)/([0-9]+)\t*')
      headerdict = dict()
      retdict = dict()
      
      for line in fileobj:
         # read first line so know how to parse
         # first is T/1, then comes the outputs
         # pattern: ([A-Za-z0-9]+)/([0-9]+)\t*
         if first:
            for(tag, length) in re.findall(p, line):               
               headerdict[tag] = int(length)
               retdict[tag] = []
            first = False
            continue
         
         # split by tab
         line = line[:-2]
         #print line.split('\t')[0]
         splitarray = [float(x) for x in line.split('\t')]
         chunkstart = 0
         # chunk according to headerdict
         for tag in headerdict.keys():
            # add to array in return dict
            length = headerdict[tag]
            #print tag + ", " + str(length)
            retdict[tag].append(splitarray[chunkstart:length])
            chunkstart += length

   return retdict

# Print iterations progress
# from: https://gist.github.com/aubricus/f91fb55dc6ba5557fbab06119420dd6a
def print_progress(iteration, total, prefix='', suffix='', decimals=1, bar_length=100):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        bar_length  - Optional  : character length of bar (Int)
    """
    str_format = "{0:." + str(decimals) + "f}"
    percents = str_format.format(100 * (iteration / float(total)))
    filled_length = int(round(bar_length * iteration / float(total)))
    bar = '|' * filled_length + '-' * (bar_length - filled_length)

    sys.stdout.write('\r%s |%s| %s%s %s' % (prefix, bar, percents, '%', suffix)),

    if iteration == total:
        sys.stdout.write('\n')
    sys.stdout.flush()
#
# 
parameter_names = \
   ["rf_size_x", "rf_size_y", "rf_inc_x", "rf_inc_y", \
   "som_size_x", "som_size_y", "alpha", "save_state", \
   "load_state", "update_weights", "filename"]

# used to build ikc files
# TODO: add span, frame, save_weights_only, load_weights_only
parameter_map_basic_old = \
   {
      "rf_size":["rf_size_x", "rf_size_y"],\
      "rf_inc": ["rf_inc_x", "rf_inc_y"],\
      "som_size": ["som_size_x", "som_size_y"],\
      #"in_som_size": ["in_som_size_x", "in_som_size_y"],\
      "alpha":["alpha"],\
      "alpha_min":["alpha_min"],\
      "alpha_decay":["alpha_decay"],\
      "save_state":["save_state"],\
      "load_state":["load_state"],\
      "update_weights":["update_weights"],\
      "filename":["filename"]
   }
parameter_map_span_old = \
{
      "span_size":["span_size_x", "span_size_y"],\
      "frame_size":["block_size_x", "block_size_y"],\
      "border_multiplier":["border_multiplier"]
}
parameter_map_basic = \
   {
      "rf_size_x":["rf_size_x"],\
      "rf_size_y":["rf_size_y"],\
      "rf_inc_x":["rf_inc_x"],\
      "rf_inc_y":["rf_inc_y"],\
      "som_size_x":["som_size_x"],\
      "som_size_y":["som_size_y"],\
      #"in_som_size": ["in_som_size_x", "in_som_size_y"],\
      "alpha":["alpha"],\
      "alpha_min":["alpha_min"],\
      "alpha_decay":["alpha_decay"],\
      "save_state":["save_state"],\
      "load_state":["load_state"],\
      "update_weights":["update_weights"],\
      "filename":["filename"]
   }
parameter_map_span = \
{
      "span_size_x":["span_size_x"],\
      "span_size_y":["span_size_y"],\
      "block_size_x":["block_size_x"],\
      "block_size_y":["block_size_y"]
}
parameter_map = dict(parameter_map_basic)

# used to do combinations
csom_parameter_values = \
   { \
      # "dataset":["cifar", "mnist"],\
      # "rf_size":[3, 5, 7, 9],\
      "rf_size":[3, 5, 7],\
      #"rf_size_x":[3, 5, 7, 9],\
      #"rf_size_y":[3, 5, 7, 9],\
      "rf_inc":[1, 3, 5],\
      #"rf_inc":[1],\
      #"rf_inc_x":[1, 3, 5, 7],\
      #"rf_inc_y":[1, 3, 5, 7],\
      "som_size":[4],\
      #"som_size_x":[4],\
      #"som_size_y":[4],\
      "alpha":[0.0001],\
   }
perc_parameter_values = \
{\
   "class_perc_train":[1, 0],\
   "rot_perc_train":[1, 0],\
   #"scale_perc_training_on":[1, 0],\
   #"trans_perc_training_on":[1, 0]
}
# training data
input_parameter_values = \
   [\
      ' input_filename="../pics/coil-100/thumbs/"' + \
         ' input_type="COIL"'+\
         ' input_size_x="32"'+\
         ' input_size_y="32"' + \
         ' input_channels="3"' +\
         ' input_classes="100"' +\
         ' input_instances="7200"' +\
         ' border_output="52"' +\
         ' border_offset="10"',\
      ' input_filename="../pics/cifar-10-batches-bin/data_batch_all.bin"' + \
         ' input_type="CIFAR"'+\
         ' input_size_x="32"'+\
         ' input_size_y="32"' + \
         ' input_channels="3"' +\
         ' input_classes="10"' +\
         ' input_instances="50000"'\
         ' border_output="32"' +
         ' border_offset="0"',\
      #' input_filename="../pics/mnist/train-images-idx3-ubyte"' + \
      #  ' input_type="MNIST"' +\
      #  ' input_size_x="28"' +\
      #  ' input_size_y="28"' +\
      #  ' input_channels="1"' +\
      #  ' input_classes="10"' +\
      #  ' input_instances="50000"'\
   ]

# transformation parameters for input data
randomizer_params_str = \
'rand_scale_min="0.5" '+\
'rand_scale_max="2.0" '+\
'rand_scale_interval="1" '+\
'rand_rot_min="-90" '+\
'rand_rot_max="90" '+\
'rand_rot_interval="1" '+\
'rand_trans_x_min="-5" '+\
'rand_trans_x_max="5" '+\
'rand_trans_x_interval="1" '+\
'rand_trans_y_min="-5" '+\
'rand_trans_y_max="5" '+\
'rand_trans_y_interval="1" '

input_path_str = "../pics/"
# layers = [1, 2, 3, 4, 5, 6]
maxlayer = 3 # 3
# pooling = [False, True]
# csom_module_file =  "csom_module.txt"
file_group_size = 10 # number of callstrings per file
#num_files = 3# number of files, which is equal to number of parallel processes/available cores
# string constants and filenames
ikc_header = readfile("ikc_header.txt")#"ikc file header"
ikc_footer = "</group>" + "\n<!-- end file -->\n"
connection_comment_str = "\t<!-- Connections -->\n"
connection_str = readfile("connection.txt") #"connection from :"
param_comment_str = "\t<!-- Parameters -->\n"
param_str = readfile("parameter.txt")
module_comment_str = "\t<!-- Modules -->\n"
csom_str = readfile("csom_pca.txt") #"csom module"
csom_name = "C" # for module naming
view_comment_str = "\t<!-- Views -->\n"
view_str = readfile("view.txt") # "view for module"
plot_str = readfile("plot.txt") # plot view
view_name_str = "\t<view name=\"Group view $name$\">\n"
shortdesc_str = "Parameterized group file for $num$ CSOM modules connected in a stack"
longdescr_str = ""
input_chan_str = readfile("input.txt")
output_chan_str = readfile("output.txt")

# csom weight params
filename_str = "filename"
load_state_str='load_state="$$"'
save_state_str='save_state="$$"'
update_weights_str='update_weights="$$"'
csom_filename_str=filename_str+'="weights/csom/$$.dat"'
perc_filename_str='perc_'+filename_str+'="weights/perceptron/$$.dat"'
pretrain_script_output_dir_str = "pretraining_scripts/"
class_train_script_output_dir_str = "class_training_scripts/"
ikaros_bin_path_str="./"
stat_data_path_str = "stat_data/"
perc_data_path_str = "perceptron/"
csom_data_path_str = "csom/"
path_str = "../Source/UserModules/Models/CSOM-paper/"

# stop criterion
# termination_str = "_termination_criterion=\"0.0008\"" # not used, use stop_criterion
subtraction_delay = '500'  # delta in ticks between t0 and t1 for 
                           # computing error gradient
stop_criterion = "0.0001" # gradient of error for stopping training

randomizer_str = \
"""
      <module
         class = "Randomizer_Group"
         name = "Rand"
      />
"""

outfile_str = \
"""
      <module
         class = "OutputFile"
         name = "OutputFile"
         _filename = "stat_data/tat_experiment_2a_train.output" 
         period="100" 
         >
         <column name = "ERROR" decimals="4"/>   
      </module>   
"""

pretrain_str = "pretrain_C"
class_train_str = "class_train_C"

# use to differentiate between fast and slow ids for L3:
#fileobj = open('l3_slow_ids.csv', 'r') # open for reading
# fileobj = open('l3_fast_ids.csv', 'r') # open for reading
#lines = fileobj.readlines() # read all lines into array
#fileobj.close()
#ok_list = [int(ln) for ln in lines]

if __name__ == '__main__':
   #tag = 'input_size_x'
   #tststr = tag + '="4"'
   #longstrval = 'input_filename="../pics/cifar-10-batches-bin/data_batch_1.bin" input_type="CIFAR" input_size_x="32" input_size_y="32" input_channels="3" input_instances="50000" C1_alpha="0.0001" C1_rf_size="3" C1_rf_inc="1" C1_som_size="4" C2_alpha="0.0001" C2_rf_size="3" C2_rf_inc="1" C2_som_size="4"' #tststr + ' C1_other="3"'
   #val = get_str_val(longstrval, tag)
   #print "get_str_val: " + val

   #retval = set_str_val(longstrval, tag, '2')
   #print "set_str_val: " + retval

   from itertools import chain, product
   tst = product(csom_parameter_values["rf_size"], csom_parameter_values["rf_inc"])
   print "rfsize\trfinc\toutput"
   for itm in tst:
      print str(itm[0]) +"\t" + str(itm[1]) + "\t" +str((32-itm[0])/itm[1] +1) +"("+str(((32-itm[0])/itm[1] +1)*4)+")"