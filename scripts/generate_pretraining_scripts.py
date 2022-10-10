#
# generates shell scripts for _executing_ pretraining of CSOMS
#
import sys, getopt
from common import *
from itertools import chain, product
# for each layer group, generate all combinations of layers and params

## TODO add parameters
# ok_list_name
# num_files

def add_check_to_callstring(callstr, layer, tag):
	'''
	Adds a check to callstring, whether output file already exists:
	if(!outputfile exists)
		run callstring
	else
		print "outputfile for ix exists, skipping"
	'''
	#tag = csom_name + str(layer) + "_" +filename_str
	p = re.compile(tag + "=" + '"(.+?)"')
	m = p.search(callstr)
	fname=m.group(1)
	fname = path_str+fname 

	p = re.compile("_([0-9]+)\-[0-9]+")
	m = p.search(callstr)
	ix = m.group(1)

	check_str = "if [ ! -f " + fname + " ]; then\n"
	execute_str = "echo " + callstr + callstr
	else_str = "else\necho;echo " + tag + " for id=" + ix +\
		" found - skipping;echo;\nfi\n\n"

	return check_str + execute_str + else_str

def gen_pretraining_scripts(ok_list, num_files):
	weight_prefix_str = "weights_"

	callstring_prefix = ikaros_bin_path_str + "ikaros "

	# callstring = "" 
	error_data_fn_str = "error_filename=\"$filename$.out\""


	keys = csom_parameter_values.keys()
	for i in xrange(1,maxlayer+1):
		csom_prefix = csom_name + str(i)
		# build a set of key-parameter strings that can be used to generate
		# combinations 
		set_collection = []
		set_collection.append(input_parameter_values)
		weight_str=""
		for layer in xrange(1, i+1):
			csom_layer_prefix = csom_name + str(layer)
			# TODO add weight parameters for each layer
			if layer == i:
				# top layer
				weight_str += " " + csom_layer_prefix + "_"+load_state_str.replace("$$", "no")
				weight_str += " " + csom_layer_prefix + "_"+save_state_str.replace("$$", "yes")
				weight_str += " " + csom_layer_prefix + "_"+update_weights_str.replace("$$", "yes")
			else:
				# not top layer
				weight_str += " " + csom_layer_prefix + "_"+load_state_str.replace("$$", "yes")
				weight_str += " " + csom_layer_prefix + "_"+save_state_str.replace("$$", "no")
				weight_str += " " + csom_layer_prefix + "_"+update_weights_str.replace("$$", "no")
			for key in keys:
				param_set = map( lambda x: csom_layer_prefix +"_" + key+"=\""+str(x)+"\"", csom_parameter_values[key] )
				set_collection.append(param_set)


			# add input set
			
			
		# create all combinations
		combinations = list(product(*set_collection))
		num_combinations = len(combinations)
		callstrings = []
		count = 1		
		for comb in combinations:
			# TODO check for valid combinations
			# if not isvalid(comb): continue

			error_data_filename_str = error_data_fn_str.replace(\
				"$filename$", \
				stat_data_path_str +\
				csom_data_path_str +\
				"error_C" + str(i) + "_" + ("_".join(comb).replace("\"", ""))+\
				"_" + str(count) + "-" + str(num_combinations) )
			# put name of dataset/input type in error str
			for param in input_parameter_values:
				error_data_filename_str = error_data_filename_str.replace(\
					param.replace("\"", ""), get_str_val(param, 'input_type'))	
			# error_data_filename_str = error_data_filename_str.replace(\
			# 	input_parameter_values[0].replace("\"", ""), "cifar")
			# error_data_filename_str = error_data_filename_str.replace(\
			# 	input_parameter_values[1].replace("\"", ""), "mnist")
			
			comb_str = " ".join(comb)
			
			#create weight filename for layers
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
					# TODO check for valid values: large receptive fields
					# and larger increments give smaller output sizes. 
					# Have to calculate valid
					# max rf size and inc based on prev layer output size
					comb_str = set_str_val(comb_str, \
						csom_name+str(layer) + "_" + "rf_size",\
						str(prev_som_size*rf_size))
					comb_str = set_str_val(comb_str, \
						csom_name+str(layer) + "_" + "rf_inc",\
						str(prev_som_size*rf_inc))
			
			# add in_som_size
					
			callstring = callstring_prefix + \
				path_str +\
				pretrain_str + str(i) + ".ikc " +\
				weight_str + " " +\
				randomizer_params_str +\
				" ".join(weight_filenames) + " " +\
				comb_str + " " +\
				error_data_filename_str + "\n" 

			# myfile.write(callstring)
			# ok_list in common.py; only add preset ids
			if len(ok_list) == 0 or count in ok_list:
				# add check if highest level weight already exist
				#tag = csom_name + str(layer) + "_" +filename_str
				#p = re.compile(tag + "=" + '"(.+?)"')
				#m = p.search(callstring)
				#fname=m.group(1)
				#fname = path_str+fname 
				#check_str = "if [ ! -f " + fname + " ]; then\n"
				#execute_str = "echo " + callstring + callstring
				#else_str = "else\necho;echo weights for id=" + str(count) +\
				#	" found - skipping;echo;\nfi\n\n"
				#callstrings.append(check_str + execute_str + else_str)
				tag = csom_name + str(layer) + "_" +filename_str
				callstr_w_check = add_check_to_callstring(callstring, layer, tag)
				callstrings.append(callstr_w_check)
			count+=1
		
		# TODO separate out and take in list of indeces to use, so can distinguish fast and slow variants
		# create chunks - note: this is more memory intensive than 
		# writing strings as you go
		# comb_chunks = list (chunks(callstrings, file_group_size))
		comb_chunks = list (chunks_num(callstrings, num_files))
		num_chunks = len(comb_chunks) # now superfluous
		# print comb_chunks
		count = 1
		for chnk in comb_chunks:
			chnk.reverse() # avoid overlap with runs on robot pc
			pretrain_file_str = \
				pretrain_script_output_dir_str +\
				pretrain_str + str(i) + "/" +\
				pretrain_str + str(i) + "_" +\
				str(count) + "-" + str(num_chunks) + ".sh"
				# TODO add tmux select and write-to-file
			writefile(pretrain_file_str, "".join(chnk))
			count+=1
			
			#with open(pretrain_file_str, "a") as myfile:
			#	for callstr in chnk
		# print " ".join(keys)
		# print " ".join(combinations[0]) + " " + termination_str
		# print callstring
		
		# print error_data_filename_str.replace("\"", "")
		print "--" # end for each max layer

def main(argv):
	okname = ''
	num_files = 0
	help_str = "syntax: generate_pretraining_scripts.py -n <num files> -f <ok file>"
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

	gen_pretraining_scripts(ok_list, num_files)


if __name__ == '__main__':
	main(sys.argv[1:])
