# 
# leaves only every 100th row of a file
#

import os
from os import listdir
from os.path import isfile, join

path = "../stat_data/csom"
outdir = "/tmp"

# expand and join path and filename

onlyfiles = [ f for f in listdir(path) if isfile(join(path,f)) and f[-3:]=="out" ]
# load file into mem

for filename in onlyfiles:
	fileandpath = os.path.join(os.path.expanduser(path), filename)
	fileobj = open(fileandpath, 'r') # open for reading
	txt = fileobj.readlines() # read all lines into a file
	fileobj.close()

	# take every 100th line
	decimated = txt[0::100]
	fileandpath = os.path.join(os.path.expanduser(path+outdir), filename+"_dec")

	fileobj = open(fileandpath, 'w')
	fileobj.write("".join(decimated))
	print "wrote " + filename + "to " + path + outdir
	fileobj.close()
