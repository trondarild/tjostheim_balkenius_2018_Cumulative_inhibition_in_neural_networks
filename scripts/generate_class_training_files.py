#
# generate class training files: class_train_C[].ikc
#

from common import *

# only topmost csom has training enabled
readdata_str = readfile("readdata.txt")
shortdesc_str = "Class training setup for $num$ CSOM modules"


longdescr_str = \
"""
	Parameters:

	class_perc_filename
	class_perc_save_state
	class_perc_load_state
	class_perc_training_on

	Cx_rf_size
	Cx_rf_inc
	Cx_som_size
	Cx_alpha
	Cx_save_state
	Cx_load_state
	Cx_update_weights
	Cx_filename
	
	error_filename - name of file to save raw error data from top level CSOM module to

	input_type - COIL, CIFAR or MNIST 
	input_filename - name of input file
	input_size_x - width
	input_size_y - height
	input_channels - number of channels (3 for RBG)
	input_instances - number of instances in file
"""

perceptron_str = \
"""
		<module
			class = "Perceptron"
			name = "$name$"
			learning_rule = "delta"
			activation_type = "tanh" 
			learning_type = "instant"
			learning_rate = "0.0005"
			correct_average_size = "50"
			_filename = "weights/tat_experiment_1a_perceptron.dat"
			_save_state = "no"
			_load_state = "yes"
	  />	
"""

perc_train_on_str =\
"""
		<module
			class="Ones"
			name="$name$"
			size_x="1"
			size_y="1"
			_value="0"
		/>
"""

stack_group_str = \
"""
		<module
			class = "$class$_group"
			name = "$name$"
		/>
"""

avg_module_str = \
"""
		<module
          class="Average"
          name="Avg"
          type="SMA"
          window_size="100"
          _termination_criterion="0.080"
      />
"""

subtract_module_str = \
"""
		<module
          class="Subtract"
          name="Subtract"
      />	
"""

stop_module_str = \
"""
		<module
			class = "Stop"
			name = "Stop"
			termination_criterion  = "$$"
			wait  = "1000000"
			select="0"
			debug="no"
		/>
"""
stop_module_str = stop_module_str.replace("$$", stop_criterion)

# names for perceptrons for class, rotation, scale and translation
class_perc_str = "ClassPerc"
class_unpert_perc_str = "ClassUnpertPerc"
rot_perc_str = "RotPerc"
scale_perc_str = "ScalePerc"
trans_perc_str = "TransPerc"
transx_perc_str = "TransXPerc"
transy_perc_str = "TransYPerc"
'''
perc_strs = [\
	class_perc_str, \
	class_unpert_perc_str,\
	rot_perc_str,\
	scale_perc_str,\
	transy_perc_str,\
	transx_perc_str\
	]
'''
train_on_str = "TrainOn"

# the base delay from file is read to it arrives at perceptron
# 5 - delay inside Dataset_input_group.ikc module due 
# to border, affine transforms and noise
class_base_delay_int = 6 
scale_base_delay_int = 4
rot_base_delay_int = 3
trans_base_delay_int = 2

# make a file for all stack sizes
for i in xrange(1,maxlayer+1):
	output_str = ""
	# add header
	header = ikc_header.replace("$title$", "Class training " + csom_name+str(i)) 
	header = header.replace("$shortdescription$", shortdesc_str.replace("$num$", str(i)))
	header = header.replace("$longdescription$", longdescr_str)
	output_str += header
	output_str+="\n\n"

	# add parameters
	output_str += param_comment_str

	p_str = param_str.replace("$target$", "filename")
	p_str = p_str.replace("$module$", class_perc_str)
	p_str = p_str.replace("$name$", "class_perc_filename")
	output_str += p_str

	p_str = param_str.replace("$target$", "filename")
	p_str = p_str.replace("$module$", rot_perc_str)
	p_str = p_str.replace("$name$", "rot_perc_filename")
	output_str += p_str

	p_str = param_str.replace("$target$", "filename")
	p_str = p_str.replace("$module$", scale_perc_str)
	p_str = p_str.replace("$name$", "scale_perc_filename")
	output_str += p_str

	p_str = param_str.replace("$target$", "filename")
	p_str = p_str.replace("$module$", transx_perc_str)
	p_str = p_str.replace("$name$", "transx_perc_filename")
	output_str += p_str

	p_str = param_str.replace("$target$", "filename")
	p_str = p_str.replace("$module$", transy_perc_str)
	p_str = p_str.replace("$name$", "transy_perc_filename")
	output_str += p_str
	

	# perceptron train
	p_str = param_str.replace("$target$", "value")
	p_str = p_str.replace("$module$", class_perc_str + train_on_str)
	p_str = p_str.replace("$name$", "perc_train")
	output_str += p_str

	p_str = param_str.replace("$target$", "value")
	p_str = p_str.replace("$module$", rot_perc_str + train_on_str)
	p_str = p_str.replace("$name$", "perc_train")
	output_str += p_str

	p_str = param_str.replace("$target$", "value")
	p_str = p_str.replace("$module$", scale_perc_str + train_on_str)
	p_str = p_str.replace("$name$", "perc_train")
	output_str += p_str

	p_str = param_str.replace("$target$", "value")
	p_str = p_str.replace("$module$", transx_perc_str + train_on_str)
	p_str = p_str.replace("$name$", "perc_train")
	output_str += p_str

	p_str = param_str.replace("$target$", "value")
	p_str = p_str.replace("$module$", transy_perc_str + train_on_str)
	p_str = p_str.replace("$name$", "perc_train")
	output_str += p_str

	# perceptron load and save
	p_str = param_str.replace("$target$", "save_state")
	p_str = p_str.replace("$module$", class_perc_str)
	p_str = p_str.replace("$name$", "perc_save_state")
	output_str += p_str

	p_str = param_str.replace("$target$", "load_state")
	p_str = p_str.replace("$module$", class_perc_str)
	p_str = p_str.replace("$name$", "perc_load_state")
	output_str += p_str
	
	p_str = param_str.replace("$target$", "save_state")
	p_str = p_str.replace("$module$", rot_perc_str)
	p_str = p_str.replace("$name$", "perc_save_state")
	output_str += p_str

	p_str = param_str.replace("$target$", "load_state")
	p_str = p_str.replace("$module$", rot_perc_str)
	p_str = p_str.replace("$name$", "perc_load_state")
	output_str += p_str

	p_str = param_str.replace("$target$", "save_state")
	p_str = p_str.replace("$module$", scale_perc_str)
	p_str = p_str.replace("$name$", "perc_save_state")
	output_str += p_str

	p_str = param_str.replace("$target$", "load_state")
	p_str = p_str.replace("$module$", scale_perc_str)
	p_str = p_str.replace("$name$", "perc_load_state")
	output_str += p_str

	p_str = param_str.replace("$target$", "save_state")
	p_str = p_str.replace("$module$", transx_perc_str)
	p_str = p_str.replace("$name$", "perc_save_state")
	output_str += p_str

	p_str = param_str.replace("$target$", "load_state")
	p_str = p_str.replace("$module$", transx_perc_str)
	p_str = p_str.replace("$name$", "perc_load_state")
	output_str += p_str

	p_str = param_str.replace("$target$", "save_state")
	p_str = p_str.replace("$module$", transy_perc_str)
	p_str = p_str.replace("$name$", "perc_save_state")
	output_str += p_str

	p_str = param_str.replace("$target$", "load_state")
	p_str = p_str.replace("$module$", transy_perc_str)
	p_str = p_str.replace("$name$", "perc_load_state")
	output_str += p_str

		# error and read dataset
	p_str = param_str.replace("$target$", "filename")
	p_str = p_str.replace("$module$", "OutputFile")
	p_str = p_str.replace("$name$", "error_filename")
	output_str += p_str

	p_str = param_str.replace("$target$", "img_filename")
	p_str = p_str.replace("$module$", "ReadDataset")
	p_str = p_str.replace("$name$", "input_filename")
	output_str += p_str

	p_str = param_str.replace("$target$", "type")
	p_str = p_str.replace("$module$", "ReadDataset")
	p_str = p_str.replace("$name$", "input_type")
	output_str += p_str

	p_str = param_str.replace("$target$", "size_x")
	p_str = p_str.replace("$module$", "ReadDataset")
	p_str = p_str.replace("$name$", "input_size_x")
	output_str += p_str

	p_str = param_str.replace("$target$", "size_y")
	p_str = p_str.replace("$module$", "ReadDataset")
	p_str = p_str.replace("$name$", "input_size_y")
	output_str += p_str

	p_str = param_str.replace("$target$", "channels")
	p_str = p_str.replace("$module$", "ReadDataset")
	p_str = p_str.replace("$name$", "input_channels")
	output_str += p_str

	p_str = param_str.replace("$target$", "instances")
	p_str = p_str.replace("$module$", "ReadDataset")
	p_str = p_str.replace("$name$", "input_instances")
	output_str += p_str

	p_str = param_str.replace("$target$", "classcount")
	p_str = p_str.replace("$module$", "ReadDataset")
	p_str = p_str.replace("$name$", "input_classes")
	output_str += p_str


	#
	# add modules
	#
	output_str += module_comment_str

	output_str += avg_module_str
	output_str += avg_module_str.replace("Avg", "StopAvg")

	output_str += subtract_module_str

	output_str += stop_module_str

	output_str += perceptron_str.replace("$name$", class_perc_str)
	output_str += perc_train_on_str.replace("$name$", class_perc_str + train_on_str)

	output_str += perceptron_str.replace("$name$", rot_perc_str)
	output_str += perc_train_on_str.replace("$name$", rot_perc_str + train_on_str)

	output_str += perceptron_str.replace("$name$", scale_perc_str)
	output_str += perc_train_on_str.replace("$name$", scale_perc_str + train_on_str)

	output_str += perceptron_str.replace("$name$", transx_perc_str)
	output_str += perceptron_str.replace("$name$", transy_perc_str)

	output_str += perc_train_on_str.replace("$name$", trans_perc_str + train_on_str)


	mod_str = stack_group_str.replace("$class$", csom_name + str(i))
	mod_str = mod_str.replace("$name$", csom_name + str(i))
	output_str += mod_str

	output_str += perc_outfile_str

	output_str += randomizer_str

	output_str += readdata_str


	#
	# add connections
	#
	output_str += connection_comment_str

	#con_str = connection_str.replace("$sourcemodule$", class_perc_str)
	#con_str = con_str.replace("$source$", "ERROR")	
	#con_str = con_str.replace("$targetmodule$", "OutputFile")
	#con_str = con_str.replace("$target$", "ERROR")
	con_str = connection_str.replace("$sourcemodule$", class_perc_str)
	con_str = con_str.replace("$source$", "CORRECT")	
	con_str = con_str.replace("$targetmodule$", "OutputFile")
	con_str = con_str.replace("$target$", "CORRECT")
	output_str += con_str

	con_str = connection_str.replace("$sourcemodule$", class_perc_str)
	con_str = con_str.replace("$source$", "CORRECT") # was ERROR	
	con_str = con_str.replace("$targetmodule$", "Avg")
	con_str = con_str.replace("$target$", "INPUT")
	output_str += con_str

	con_str = connection_str.replace("$sourcemodule$", "Avg")
	con_str = con_str.replace("$source$", "OUTPUT")	
	con_str = con_str.replace("$targetmodule$", "Subtract")
	con_str = con_str.replace("$target$", "INPUT2")
	output_str += con_str

	con_str = connection_str.replace("$sourcemodule$", "Avg")
	con_str = con_str.replace("$source$", "OUTPUT")	
	con_str = con_str.replace("$targetmodule$", "Subtract")
	con_str = con_str.replace("$target$", "INPUT1")
	con_str = con_str.replace('delay="1"', 'delay="' + subtraction_delay + '"')
	output_str += con_str

	con_str = connection_str.replace("$sourcemodule$", "Subtract")
	con_str = con_str.replace("$source$", "OUTPUT")	
	con_str = con_str.replace("$targetmodule$", "StopAvg")
	con_str = con_str.replace("$target$", "INPUT")
	output_str += con_str

	con_str = connection_str.replace("$sourcemodule$", "StopAvg")
	con_str = con_str.replace("$source$", "OUTPUT")	
	con_str = con_str.replace("$targetmodule$", "Stop")
	con_str = con_str.replace("$target$", "INPUT")
	output_str += con_str

	con_str = connection_str.replace("$sourcemodule$", "ReadDataset")
	con_str = con_str.replace("$source$", "OUTPUT")
	con_str = con_str.replace("$targetmodule$", csom_name + str(i))
	con_str = con_str.replace("$target$", "INPUT")
	output_str += con_str

	con_str = connection_str.replace("$sourcemodule$", "Rand")
	con_str = con_str.replace("$source$", "SCALE_OUTPUT")
	con_str = con_str.replace("$targetmodule$", "ReadDataset")
	con_str = con_str.replace("$target$", "SCALE")
	output_str += con_str

	con_str = connection_str.replace("$sourcemodule$", "Rand")
	con_str = con_str.replace("$source$", "ROTATION_OUTPUT")
	con_str = con_str.replace("$targetmodule$", "ReadDataset")
	con_str = con_str.replace("$target$", "ROTATION")
	output_str += con_str

	con_str = connection_str.replace("$sourcemodule$", "Rand")
	con_str = con_str.replace("$source$", "TRANSX_OUTPUT")
	con_str = con_str.replace("$targetmodule$", "ReadDataset")
	con_str = con_str.replace("$target$", "TRANS_X")
	output_str += con_str

	con_str = connection_str.replace("$sourcemodule$", "Rand")
	con_str = con_str.replace("$source$", "TRANSY_OUTPUT")
	con_str = con_str.replace("$targetmodule$", "ReadDataset")
	con_str = con_str.replace("$target$", "TRANS_Y")
	output_str += con_str

	con_str = connection_str.replace("$sourcemodule$", csom_name + str(i))
	con_str = con_str.replace("$source$", "OUTPUT")
	con_str = con_str.replace("$targetmodule$", class_perc_str)
	con_str = con_str.replace("$target$", "INPUT")
	output_str += con_str

	con_str = connection_str.replace("$sourcemodule$", csom_name + str(i))
	con_str = con_str.replace("$source$", "OUTPUT")
	con_str = con_str.replace("$targetmodule$", class_perc_str)
	con_str = con_str.replace("$target$", "T_INPUT")
	output_str += con_str

	con_str = connection_str.replace("$sourcemodule$", "ReadDataset")
	con_str = con_str.replace("$source$", "CLASS")
	con_str = con_str.replace("$targetmodule$", class_perc_str)
	con_str = con_str.replace("$target$", "T_TARGET")
	con_str = con_str.replace('delay="1"', 'delay="'+str(i+class_base_delay_int) + '"')
	output_str += con_str

	con_str = connection_str.replace("$sourcemodule$", class_perc_str + train_on_str)
	con_str = con_str.replace("$source$", "OUTPUT")
	con_str = con_str.replace("$targetmodule$", class_perc_str)
	con_str = con_str.replace("$target$", "TRAIN")
	output_str += con_str

	con_str = connection_str.replace("$sourcemodule$", csom_name + str(i))
	con_str = con_str.replace("$source$", "OUTPUT")
	con_str = con_str.replace("$targetmodule$", rot_perc_str)
	con_str = con_str.replace("$target$", "INPUT")
	output_str += con_str

	con_str = connection_str.replace("$sourcemodule$", csom_name + str(i))
	con_str = con_str.replace("$source$", "OUTPUT")
	con_str = con_str.replace("$targetmodule$", rot_perc_str)
	con_str = con_str.replace("$target$", "T_INPUT")
	output_str += con_str

	con_str = connection_str.replace("$sourcemodule$", "Rand")
	con_str = con_str.replace("$source$", "ROTATION_OUTPUT")
	con_str = con_str.replace("$targetmodule$", rot_perc_str)
	con_str = con_str.replace("$target$", "T_TARGET")
	con_str = con_str.replace('delay="1"', 'delay="'+str(i+rot_base_delay_int) + '"')
	output_str += con_str

	con_str = connection_str.replace("$sourcemodule$", rot_perc_str + train_on_str)
	con_str = con_str.replace("$source$", "OUTPUT")
	con_str = con_str.replace("$targetmodule$", rot_perc_str)
	con_str = con_str.replace("$target$", "TRAIN")
	output_str += con_str

	con_str = connection_str.replace("$sourcemodule$", csom_name + str(i))
	con_str = con_str.replace("$source$", "OUTPUT")
	con_str = con_str.replace("$targetmodule$", scale_perc_str)
	con_str = con_str.replace("$target$", "INPUT")
	output_str += con_str

	con_str = connection_str.replace("$sourcemodule$", csom_name + str(i))
	con_str = con_str.replace("$source$", "OUTPUT")
	con_str = con_str.replace("$targetmodule$", scale_perc_str)
	con_str = con_str.replace("$target$", "T_INPUT")
	output_str += con_str

	con_str = connection_str.replace("$sourcemodule$", "Rand")
	con_str = con_str.replace("$source$", "SCALE_OUTPUT")
	con_str = con_str.replace("$targetmodule$", scale_perc_str)
	con_str = con_str.replace("$target$", "T_TARGET")
	con_str = con_str.replace('delay="1"', 'delay="'+str(i+scale_base_delay_int) + '"')
	output_str += con_str

	con_str = connection_str.replace("$sourcemodule$", scale_perc_str + train_on_str)
	con_str = con_str.replace("$source$", "OUTPUT")
	con_str = con_str.replace("$targetmodule$", scale_perc_str)
	con_str = con_str.replace("$target$", "TRAIN")
	output_str += con_str

	con_str = connection_str.replace("$sourcemodule$", csom_name + str(i))
	con_str = con_str.replace("$source$", "OUTPUT")
	con_str = con_str.replace("$targetmodule$", transx_perc_str)
	con_str = con_str.replace("$target$", "INPUT")
	output_str += con_str

	con_str = connection_str.replace("$sourcemodule$", csom_name + str(i))
	con_str = con_str.replace("$source$", "OUTPUT")
	con_str = con_str.replace("$targetmodule$", transx_perc_str)
	con_str = con_str.replace("$target$", "T_INPUT")
	output_str += con_str

	con_str = connection_str.replace("$sourcemodule$", "Rand")
	con_str = con_str.replace("$source$", "TRANSX_OUTPUT")
	con_str = con_str.replace("$targetmodule$", transx_perc_str)
	con_str = con_str.replace("$target$", "T_TARGET")
	con_str = con_str.replace('delay="1"', 'delay="'+str(i+trans_base_delay_int) + '"')
	output_str += con_str


	con_str = connection_str.replace("$sourcemodule$", trans_perc_str + train_on_str)
	con_str = con_str.replace("$source$", "OUTPUT")
	con_str = con_str.replace("$targetmodule$", transx_perc_str)
	con_str = con_str.replace("$target$", "TRAIN")
	output_str += con_str

	con_str = connection_str.replace("$sourcemodule$", csom_name + str(i))
	con_str = con_str.replace("$source$", "OUTPUT")
	con_str = con_str.replace("$targetmodule$", transy_perc_str)
	con_str = con_str.replace("$target$", "INPUT")
	output_str += con_str

	con_str = connection_str.replace("$sourcemodule$", csom_name + str(i))
	con_str = con_str.replace("$source$", "OUTPUT")
	con_str = con_str.replace("$targetmodule$", transy_perc_str)
	con_str = con_str.replace("$target$", "T_INPUT")
	output_str += con_str

	con_str = connection_str.replace("$sourcemodule$", "Rand")
	con_str = con_str.replace("$source$", "TRANSY_OUTPUT")
	con_str = con_str.replace("$targetmodule$", transy_perc_str)
	con_str = con_str.replace("$target$", "T_TARGET")
	con_str = con_str.replace('delay="1"', 'delay="'+str(i+trans_base_delay_int) + '"')
	output_str += con_str


	con_str = connection_str.replace("$sourcemodule$", trans_perc_str + train_on_str)
	con_str = con_str.replace("$source$", "OUTPUT")
	con_str = con_str.replace("$targetmodule$", transy_perc_str)
	con_str = con_str.replace("$target$", "TRAIN")
	output_str += con_str

	output_str += ikc_footer

#if __name__ == '__main__':
	# print output_str
	writefile("../class_train_" + csom_name + str(i) + ".ikc", output_str)