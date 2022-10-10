#!/usr/bin/python
# script for generating a startup script for tmux with given grid
# params:
# -n: name of session
# -col: number of columns
# -row: number of rows

import sys, getopt
from itertools import product
from common import *

def gen_splits(p_frac):
	# generate a list of percentages based on a fraction
	frac = p_frac
	retval = []
	while frac > 1:
		retval.append(100/frac)
		frac = frac - 1
	return retval

def generate_tmux_session(name, rows, cols, prefix, postfix):
	# generates tmux commands to set up tmux with a grid and execute
	# a command in each pane
	retval = ""
	retval += "tmux new-session -d -s " + name + "\n"
	retval += "tmux rename-window '" + name + "'" + "\n"
	
	counter = 1
	col_fracs = gen_splits(cols)
	retval += "tmux send-keys \"" + prefix + str(counter) + postfix \
			+ "\"" + " Enter" + "\n"
	counter += 1
	for spl in col_fracs:
		retval += "tmux split-window -h -p " + str(spl) + "\n"
		retval += "tmux send-keys \"" + prefix + str(counter) + postfix \
			+ "\"" + " Enter" + "\n"
		counter += 1
		retval += "tmux select-pane -L # go left" + "\n"

	
	row_fracs = gen_splits(rows)
	for col in range(1, cols+1):
		for spl in row_fracs:
			retval += "tmux split-window -v -p " + str(spl) + "\n"
			retval += "tmux send-keys \"" + prefix + str(counter) + postfix \
				+ "\"" + " Enter" + "\n"
			counter += 1
			retval += "tmux select-pane -U # go up"		 + "\n"
		retval += "\n"
		retval += "tmux select-pane -R # go right and repeat" + "\n"
	retval += "\n"
	retval += "tmux attach-session -t " + name + "\n"
	return retval


# note: convert to function?
def main(argv):
	name = ''
	rows = 0
	cols = 0
	path_str = "../Source/UserModules/Models/CSOM-paper/scripts/"
	prefix = "sh " + path_str
	

	helpstr = 'syntax: tmux-session.py -r <rows> -c <cols>' 
	try:
		opts, args = getopt.getopt(argv,"hc:r:",["help", "col=", "row="])
		# print opts
		# print args
	except getopt.GetoptError:
		print helpstr
		sys.exit(2)
	for opt, arg in opts:
		if opt == '-h':
			print helpstr
			sys.exit()
		# elif opt in ("-n", "--name"):
		# 	name = arg
		elif opt in ("-c", "--col"):
			cols = int(arg)
		elif opt in ("-r", "--row"):
			rows = int(arg)  
		# elif opt in ("-p", "--prefix"):
		# 	prefix = arg
		# elif opt in ("-o", "--postfix"):
		# 	postfix = arg
	# generate tmux commands      
	postfix = "-" + str(rows*cols) + ".sh"
	conditions = ["pretrain", "class_train"]
	layers = [i for i in range (1, maxlayer+1)]
	prod = product(conditions, layers)
	for i in prod:
		cond_str = i[0] + "_C" + str(i[1])
		prefix_str = prefix + i[0] + "ing_scripts/" + \
			cond_str + "/" + cond_str + "_"
		# combination of condition and layer
		name = cond_str
		tmux_str = generate_tmux_session(name, rows, cols, prefix_str, postfix)
		# write to file
		fname = i[0] + "ing_scripts/" + \
			cond_str + "/tmux-" + cond_str + ".sh"
		# print fname
		# print tmux_str
		writefile(fname, tmux_str)
		print "tmux session files written to " + fname



if __name__ == "__main__":
	# print gen_splits(8)
	# print sys.argv[1:]
	main(sys.argv[1:])
