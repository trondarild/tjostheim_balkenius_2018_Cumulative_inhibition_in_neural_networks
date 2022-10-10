#
# visualization of csom weights
#

import sys, getopt
import numpy as np
from common import *
from os import listdir
from os.path import isfile, join
import png
# param: path to weight files
# param: max layer level

def get_input_sz(inp):
	retval = 0
	if 'CIFAR' in inp:
		retval = 32
	elif 'COIL' in inp:
		retval = 52
	return retval



def check_name(name, layerix, rfsz, rfinc, somsz, inptype):
	params = ["C" + str(layerix) + "_rf_size=" + str(rfsz),\
		"C" + str(layerix) + "_rf_inc=" + str(rfinc),\
		"C" + str(layerix) + "_som_size=" + str(somsz),\
		inptype]
	ok = True
	for p in params:
		ok = ok and p in name
	return ok


def deserialize2d(fobj, rows, cols):
	retval = np.zeros((rows, cols))
	#fileobj = open(fname, 'r')
	for j in range(rows):
		for i in range(cols):
			retval[j][i] = float(fobj.read())
	#fileobj.close
	return retval


def deserialize4d(fobj, rowouter, colouter, rowinner, colinner, begin, end):
	#retval = np.zeros((rowouter, colouter, rowinner, colinner))
	#for j in range(rowouter):
	#	for i in range(colouter):
	#		retval[j][i] = deserialize2d(fobj, rowinner, colinner)
	tmp = fobj.read().split("\t")
	
	tmp = [float(x) for x in tmp if x!='']
	tmp = np.asarray(tmp)
	tmp = tmp[begin:end]
	
	
	tmp.shape=(rowouter, colouter, rowinner, colinner)
	return tmp

def readweights(fileandpath, rfszx, rfszy, rfincx, rfincy, somszx, somszy):
	sz = get_input_sz(fileandpath)
	fileobj = open(fileandpath, 'r')
	# TODO put into function:
	mapsizex = (sz-rfszx)/rfincx + 1
	mapsizey = (sz-rfszy)/rfincy + 1
	begin = somszx*somszy*mapsizex*mapsizey
	end = somszx*somszy*rfszx*rfszy
	weights = deserialize4d(fileobj, somszy, somszx,\
		rfszy, rfszx,\
		begin, begin+end)
	fileobj.close()
 
	return weights

def regenerate(inp, out_x, out_y, mpx, mpy, somx, somy, rfx, rfy, rfincx, rfincy, w):

	out_reconstruction = np.zeros((out_y, out_x))

	for mj in xrange(0, mpy):
		for mi in xrange(0, mpx):
		  
			for sj in xrange(0, somy):
				for si in xrange(0, somx):
				 	for ri in xrange(0, rfx):
						for rj in xrange(0, rfy):
							out_reconstruction[rfincy*mj+rj][rfincx*mi+ri] +=\
							  inp[mj*somy+sj][mi*somx+si] * w[sj][si][rj][ri]

	#out_reconstruction = np.abs(out_reconstruction)
	#out_reconstruction *=255.0/out_reconstruction.max()
	return out_reconstruction


def generate_top_down(path, wfile, winfo, maxlayer, topdown, mpx, mpy):
		# print "maxlayer=" + str(maxlayer)
		# print "topdown[0][0]:"
		# print topdown[0][0]
		# print "mp=" + str(mpx)

		# TODO if maxlayer > 1, also read required files for lower layers
		fileandpath = os.path.join(os.path.expanduser(path), wfile)
		rfsz = winfo['C'+str(maxlayer)+'_rf_size']
		rfinc = winfo['C'+str(maxlayer)+'_rf_inc']
		nextrf = 0
		nextinc = 0
		if maxlayer > 1:
			rfsz *= winfo['C'+str(maxlayer-1)+'_som_size']
			rfinc *= winfo['C'+str(maxlayer-1)+'_som_size']
			nextrf = winfo['C'+str(maxlayer-1)+'_rf_size']
			nextinc = winfo['C'+str(maxlayer-1)+'_rf_inc']
			# count down and go again
			# calculate size rf fields in pixels:
			# rfpix = prev_somsz*rfunits
			
		somsz = winfo['C'+str(maxlayer)+'_som_size']
		weights = readweights(fileandpath, rfsz, rfsz,\
			rfinc, rfinc,\
			somsz, somsz)


		#nextweights = readweights(nextfileandpath, nextrf, nextrf,\
		#		nextinc, nextinc, nextsomsz, nextsomsz)	
		regensz = rfsz if topdown[0][0].shape[0] == somsz else rfinc*mpx+rfsz
		regenweights = np.zeros((somsz, somsz, regensz, regensz))
		#nextregenweights = np.zeros((nextsomsz, nextsomsz, nextinc*winfo['C'+str(maxlayer)+'_rf_size']+nextrf, nextinc*winfo['C'+str(maxlayer)+'_rf_size']+nextrf))
		for j in xrange(0, somsz):
			for i in xrange(0, somsz):
				# topdown = np.zeros((somsz, somsz))
				# topdown[j][i] = 1.0
				weight = weights[j][i]
				#mpx = mpy = 1#winfo['C'+str(maxlayer)+'_rf_size']
				regenweight = regenerate(topdown[j][i], regensz, regensz, mpx, mpy, somsz, somsz,\
					rfsz, rfsz, rfinc, rfinc, weights)					
				regenweights[j][i] = regenweight
				# mpx = mpy = winfo['C'+str(maxlayer)+'_rf_size']
				# nextregenweight = regenerate(regenweight, nextinc*mpx+nextrf, nextinc*mpx+nextrf, mpx, mpy, nextsomsz, nextsomsz,\
				# 	nextrf, nextrf, nextinc, nextinc, nextweights)
				# nextregenweights[j][i] = nextregenweight
		if maxlayer > 1: 
			
			nextsomsz = winfo['C'+str(maxlayer-1)+'_som_size']
			nextweightfile = [ f for f in listdir(path)\
				if isfile(join(path,f)) and int(f[1]) == maxlayer-1\
				and check_name(f, maxlayer-1, nextrf, nextinc, nextsomsz, get_input_tag(wfile))]
			#nextfileandpath = os.path.join(os.path.expanduser(path), nextweightfile[0])
			
			regenweights = generate_top_down(path, nextweightfile[0], winfo, maxlayer-1, regenweights,\
					winfo['C'+str(maxlayer)+'_rf_size'],\
					winfo['C'+str(maxlayer)+'_rf_size'])
		
		return regenweights	
			

def generate_weight_image(somszx, somszy, rfszx, rfszy, w):
	weight_image = np.zeros((somszy*rfszy, \
				somszx*rfszx))
	
	for j in xrange(0, somszy):
		for i in xrange(0, somszx):
			tmp = np.abs(w[j][i])
			tmp *= 255.0/tmp.max() if tmp.max() > 0.0 else 0.0
			for jj in xrange(0, rfszy):
				for ii in xrange(0, rfszx):
					jix = j*rfszy + jj
					iix = i*rfszx + ii
					weight_image[jix][iix] = tmp[jj][ii]
	return weight_image

def write_image(fname, width, height, data):
	f = open(fname+'.png', 'wb') 
	w = png.Writer(width, \
			height, greyscale=True)
	w.write(f, data)
	f.close()
			

def main(argv):
	path = ''
	maxlayer = 0
	imgpath = ''
	help_str = "syntax: generate_classtraining_scripts.py -p <path to weight files> -l <max layer>"
	try:
		opts, args = getopt.getopt(argv, "hp:l:i:", ["help", "path=", "maxlayer=", "imgpath="])
	except getopt.GetoptError:
		print help_str
		sys.exit(2)
	for opt, arg in opts:
		if opt=="-h":
			print help_str
			sys.exit()
		elif opt in ("-p", "--path"):
			path = arg
		elif opt in ("-l", "--maxlayer"):
			maxlayer = int(arg)
		elif opt in ("-i", "--imgpath"):
			imgpath = arg

	donefiles = [ f for f in listdir(imgpath) \
		if f[0] != '.' and isfile(join(imgpath,f)) and int(f[1]) == maxlayer]
	print "already processed: " + str(len(donefiles))
	# read all files for maxlayer
	weightfiles = [ f for f in listdir(path) \
		if isfile(join(path,f)) and int(f[1]) == maxlayer and not (f+".png" in donefiles)]
	print "files to process: " + str(len(weightfiles))
	ctr = 1
	for wfile in weightfiles:
		#fileandpath = os.path.join(os.path.expanduser(path), wfile)
		
		winfo=parsefilename(wfile, maxlayer)

		# TODO if maxlayer > 1, also read required files for lower layers
		
		somsz = winfo['C'+str(maxlayer)+'_som_size']
		topdown = np.zeros((somsz, somsz, somsz, somsz))
		for j in xrange(0, somsz):
			for i in xrange(0, somsz):
				topdown[j][i][j][i] = 1.0
		regenweights = generate_top_down(path, wfile, winfo,\
			maxlayer, topdown, 1, 1)
		#weightimage = generate_weight_image(somsz, somsz, rfsz, rfsz, regenweights)
		l1somsz = winfo['C1_som_size']
		l1inc = winfo['C1_rf_inc']
		l1rf = winfo['C1_rf_size']
		mpsz = regenweights[0][0].shape[0] #1 if maxlayer == 1 else winfo['C2_rf_size']
		weightimage = generate_weight_image(l1somsz, l1somsz, mpsz, mpsz, regenweights)
		#write_image(wfile, somsz*rfsz, somsz*rfsz, np.nan_to_num(weightimage))
		write_image(join(imgpath, wfile), l1somsz*mpsz, l1somsz*mpsz, np.nan_to_num(weightimage))
		print str (ctr) + "/" + str(len(weightfiles)) + " done"
		ctr+=1


if __name__ == '__main__':
	#main(sys.argv[1:])
	main(["-p/Users/tr1445tj/Code/ikaros/ik-t-tst/Source/UserModules/Models/CSOM-paper/weights/csom", "-l3", "-iweight_images"])
