#
# generates shell scripts for _executing_ class training of perceptrons
# connected to  CSOMS
#
import sys, getopt
from common import *
from itertools import chain, product
# for each layer group, generate all combinations of layers and params

def gen_callstrings(ok_list, max_layer):
	'''
	Generate callstrings with ids in ok_list and for given max_layer
	'''

	weight_prefix_str = "weights_"
	percs = ('class', 'rot', 'scale', 'transx', 'transy')

	# remove -s4 for production
	callstring_prefix = ikaros_bin_path_str + "ikaros "
	perc_save_state_str = 'perc_save_state="yes"'
	perc_load_state_str = 'perc_load_state="no"'
	perc_train_str = 'perc_train="1"'
	# callstring = "" 
	error_data_fn_str = "error_filename=\"$filename$.out\""

	# make set of perceptron params
	perc_collection=[]
	perc_keys = perc_parameter_values.keys()
	for key in perc_keys:
		param_set = map(lambda x: key+"=\""+str(x)+"\"", perc_parameter_values[key])
		perc_collection.append(param_set)

	keys = csom_parameter_values.keys()


	i = max_layer
	#for i in xrange(1,maxlayer+1):

	# TODO adapt so correct params are set for each layer - 
	# only topmost layer should update weights and save state
	csom_prefix = csom_name + str(i)
	# build a set of key-parameter strings that callstringn be used to generate
	# combinations 
	set_collection = []
	set_collection.append(input_parameter_values)
	for x in perc_collection:
		set_collection.append(x)
	weight_str=""
	for layer in xrange(1, i+1):
		csom_layer_prefix = csom_name + str(layer)
		
		# load but no save
		weight_str += " " + csom_layer_prefix + "_"+load_state_str.replace("$$", "yes")
		weight_str += " " + csom_layer_prefix + "_"+save_state_str.replace("$$", "no")
		weight_str += " " + csom_layer_prefix + "_"+update_weights_str.replace("$$", "no")
		for key in keys:
			param_set = map( lambda x: csom_layer_prefix +"_" + key+"=\""+str(x)+"\"", csom_parameter_values[key] )
			set_collection.append(param_set)

		
	# create all combinations
	combinations = list(product(*set_collection))
	num_combinations = len(combinations)
	callstrings = []
	# TODO divide set into n parts and write separate files
	count = 1		
	for comb in combinations:
		
		error_data_filename_str = error_data_fn_str.replace(\
			"$filename$", \
			stat_data_path_str +\
			perc_data_path_str +\
			"error_perc_C" + str(i) + "_" + ("_".join(comb).replace("\"", ""))+\
			"_" + str(count) + "-" + str(num_combinations) )
		# put name of dataset/input type in error str
		for param in input_parameter_values:
			error_data_filename_str = error_data_filename_str.replace(\
				param.replace("\"", ""), get_str_val(param, 'input_type'))	
		
		comb_str = " ".join(comb)
		
		perc_weight_filename_str = ""
		#create weight filename for csom layers (perceptron has separate filename)
		paramlst_str=""
		prev_paramlst_str=""
		weight_filenames = []
		for layer in xrange(1, i+1):
			prev_paramlst_str += paramlst_str
			match = [x for x in comb\
				if (csom_name+str(layer) in x)]
			paramlst_str = ("_".join(match)).replace("\"", "")
			fn_str = csom_name + str(layer) + "_" +\
				csom_filename_str.replace("$$", \
				csom_name + str(layer) + "_" +\
				weight_prefix_str +\
				get_str_val(comb_str, "input_type") +\
				prev_paramlst_str + "_" + paramlst_str)
			weight_filenames.append(fn_str)

			if layer == i:
				perc_weight_filename_str =\
					get_str_val(comb_str, "input_type") + "_" +\
					prev_paramlst_str + "_" + paramlst_str

			# get value of previous som size and multiply it with  rf_size and rf_inc
			if layer > 1:
				# get som size
				prev_som_size = int (get_str_val(comb_str,\
					csom_name+str(layer-1) + "_" + "som_size"))
				# get rf_size
				rf_size = int(get_str_val(comb_str,\
					csom_name+str(layer) + "_" + "rf_size"))
				# get rf_inc
				rf_inc = int(get_str_val(comb_str,\
					csom_name+str(layer) + "_" + "rf_inc"))

				# set new values
				comb_str = set_str_val(comb_str, \
					csom_name+str(layer) + "_" + "rf_size",
					str(prev_som_size*rf_size))
				comb_str = set_str_val(comb_str, \
					csom_name+str(layer) + "_" + "rf_inc",
					str(prev_som_size*rf_inc))
		

		# compose perceptron weight filenames
		# TODO: generate from ["class", "rot", "scale", "trans"]
		perc_weight_filenames=[]
		for perc in percs:
			perc_weight_filenames.append(\
				 perc+"_" +\
				 perc_filename_str.replace("$$",\
					csom_name + str(layer) + "_" +\
					perc+"_perc_" +\
					perc_weight_filename_str))
			
		

		# add in_som_size
		if len(ok_list) == 0 or count in ok_list:		
			# TODO add rot scale trans info			
			callstring = callstring_prefix + \
				path_str +\
				class_train_str + str(i) + ".ikc " +\
				weight_str + " " +\
				" ".join(perc_weight_filenames) + " " +\
				perc_save_state_str + " " +\
				perc_load_state_str + " " +\
				perc_train_str + " " +\
				randomizer_params_str +\
				" ".join(weight_filenames) + " " +\
				comb_str + " " +\
				error_data_filename_str + "\n" 

			# myfile.write(callstring)
			callstrings.append(callstring)
		count+=1
	return callstrings
			
def gen_classtraining_scripts(ok_list, num_files, max_layer):	
	'''
	Chunk callstrings and write them to files
	'''
	for i in xrange(1,max_layer+1):	
		callstrings = gen_callstrings(ok_list, max_layer)
		# create chunks - note: this is more memory intensive than 
		# writing strings as you go
		# comb_chunks = list (chunks(callstrings, file_group_size))
		comb_chunks = list (chunks_num(callstrings, num_files))
		num_chunks = len(comb_chunks) # now superfluous
		# print comb_chunks
		count = 1
		for chnk in comb_chunks:
			class_train_file_str = \
				class_train_script_output_dir_str +\
				class_train_str + str(i) + "/" +\
				class_train_str + str(i) + "_" +\
				str(count) + "-" + str(num_chunks) + ".sh"
			writefile(class_train_file_str, "".join(chnk))
			count+=1
			
			#with open(class_train_file_str, "a") as myfile:
			#	for callstr in chnk
		# print " ".join(keys)
		# print " ".join(combinations[0]) + " " + termination_str
		# print callstring
		
		# print error_data_filename_str.replace("\"", "")
		print "--"

def main(argv):
	randomizer_params_str = \
	'rand_scale_min="1" '+\
	'rand_scale_max="1.0" '+\
	'rand_scale_interval="1" '+\
	'rand_rot_min="0" '+\
	'rand_rot_max="0" '+\
	'rand_rot_interval="1" '+\
	'rand_trans_x_min="0" '+\
	'rand_trans_x_max="0" '+\
	'rand_trans_x_interval="1" '+\
	'rand_trans_y_min="0" '+\
	'rand_trans_y_max="0" '+\
	'rand_trans_y_interval="1" '

	okname = ''
	num_files = 0
	help_str = "syntax: generate_classtraining_scripts.py -n <num files> -f <ok file>"
	try:
		opts, args = getopt.getopt(argv, "hn:f:", ["help", "num=", "file="])
	except getopt.GetoptError:
		print help_str
		sys.exit(2)
	for opt, arg in opts:
		if opt=="-h":
			print help_str
			sys.exit()
		elif opt in ("-n", "--num"):
			num_files = int(arg)
		elif opt in ("-f", "--file"):
			okname = arg

	# read ok file
	fileobj = open(okname, 'r') # open for reading
	ok_list = fileobj.readlines() # read all lines into array
	fileobj.close()
	ok_list = [int(ln) for ln in ok_list]

	gen_classtraining_scripts(ok_list, num_files, maxlayer)

if __name__ == '__main__':
	main(sys.argv[1:])
