#
# stats on csom and perceptron
#
from os import listdir, stat
from os.path import isfile, join
import sys
import common as cmn
import numpy as np
import pandas as pd
import ggplot as gg
import matplotlib.pyplot as mp

def ggplt(dframe):
	#lngdf = pd.melt(dframe[['ix', 'perc_error_mean']], id_vars=['ix'])
	#print lngdf
	p = gg.ggplot(gg.aes(x='ix', y='perc_error_mean'), data=dframe) + gg.geom_bar()
	
	print p

def mplt(dframe):
	ax = mp.subplot()
	num = dframe.shape[0]

	ind = np.arange(num)
	bar = ax.bar(ind, dframe['perc_error_mean'], 0.35, yerr=dframe['perc_error_sd'])
	mp.show()

def main(argv):
	maxlayer = 3
	datalen = 1000
	errorcol_name = "ERROR/1"
	perc_path = "../stat_data/perceptron"

	# create dataframe for holding all combinations
	# TODO - add running length in time, running lenght in ticks
	# CSOM error?
	cols = ["ix",\
			"input",\
			"rf1",\
			"inc1",\
			"rf2",\
			"inc2",\
			"rf3",\
			"inc3",\
			"perc_error_mean",\
			"perc_error_sd"\
		]
	combdf = pd.DataFrame(columns = cols)
	# read all stat files in directory
	percfiles = [ f for f in listdir(perc_path) \
		if f[0] != '.' and isfile(join(perc_path,f)) and\
		int(f[12]) == maxlayer and stat(join(perc_path,f)).st_size > 0]
	print "files to process: " + str(len(percfiles))
	for pfile in percfiles:
		# parse filename
		finfo = cmn.parsefilename(pfile, maxlayer)
		inp = cmn.get_input_tag(pfile)
		# read using pandas into dataframe
		df = pd.read_table(join(perc_path, pfile))
		col = df[errorcol_name]
		tail = col.tail(datalen)
		mean = tail.mean()
		std = tail.std()
		combdf.loc[combdf.shape[0]] = [
			finfo['ix'],\
			finfo['input'],\
			finfo['C1_rf_size'],\
			finfo['C1_rf_inc'],\
			finfo['C2_rf_size'],\
			finfo['C2_rf_inc'],\
			finfo['C3_rf_size'],\
			finfo['C3_rf_inc'],\
			mean,\
			std\
		]
		#print df.shape[0]
	#print combdf.describe()
	#mplt(combdf)
		

	# get summary stats: mean and SD

if __name__ == '__main__':
	main(sys.argv[1:])
