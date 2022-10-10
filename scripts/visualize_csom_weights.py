#
# visualization of csom weights
# 2017-09-01: update to handle 
#

import sys, getopt
from operator import div
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
'''
def check_name(name, layerix, som, rf, inc, inptype):
	# 
	params = ["C" + str(layerix) + "rf_size=" + str(rf),\
				"C" + str(layerix) + "inc_size=" + str(inc),\
				"C" + str(layerix) + "som_size=" + str(som),\
				inptype]
	ok = True
	for p in params:
		ok = ok and p in name
	return ok
'''
# TODO
def check_name(name, layerix, somx, somy, rfx, rfy, rfincx, rfincy, blockx, blocky, spanx, spany, inptype):
	# extract substring for layer
	p = re.compile("C" + str(layerix) + '\(([0-9a-z\(\)_\-]+)\)?')
	m = p.search(name)
	if m == None:
		print 'no match!'
		return False
	substr = m.group(1)
	# print 'substr =' + substr
	

	params = ["rf(" + str(rfx) + "-" + str(rfy) + ")",\
		"inc(" + str(rfincx) + "-" + str(rfincy) + ")",\
		"som(" + str(somx) + "-" + str(somy) + ")",\
		"span(" + str(spanx) + "-" + str(spany) + ")",\
		"block(" + str(blockx) + "-" + str(blocky) + ")"]
	ok = inptype in name
	for p in params:
		check = p in substr
		if not check: print 'failed: ' + p 
		ok = ok and check
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
	# print "tmp length: " + str(len(tmp))
	tmp = tmp[begin:end]
	
	
	tmp.shape=(rowouter, colouter, rowinner, colinner)
	return tmp

def readweights(fileandpath, rfszx, rfszy, somszx, somszy):
	#sz = get_input_sz(fileandpath)
	fileobj = open(fileandpath, 'r')
	# no longer have to skip anything
	#mapsizex = (sz-rfszx)/rfincx + 1
	#mapsizey = (sz-rfszy)/rfincy + 1
	#begin = somszx*somszy*mapsizex*mapsizey
	#end = somszx*somszy*rfszx*rfszy
	begin = 0
	end = rfszx*rfszy*somszx*somszy
	# print fileandpath
	# print 'end= ' + str(end), 'product= ' + str(rfszx*rfszy*somszx*somszy)
	weights = deserialize4d(fileobj, somszy, somszx,\
		rfszy, rfszx,\
		begin, begin+end)
	fileobj.close()
 
	return weights

def regenerate(inp, out_x, out_y, mpx, mpy, somx, somy, rfx, rfy, rfincx, rfincy, blockx, blocky, spanx, spany, w):
	out_reconstruction = np.zeros((out_y, out_x))
	#print 'w.shape=' + str(w.shape[0])
	#print 'rfx=' + str(rfx) + ', rfy=' + str(rfy)
	for mj in xrange(0, mpy):
		for mi in xrange(0, mpx):
		  
			for sj in xrange(0, somy):
				for si in xrange(0, somx):
				 	for ri in xrange(0, rfx):
				 		dv_x = div(ri, blockx)
				 		offset_x = dv_x * spanx
						for rj in xrange(0, rfy):
							try:
								ox = rfincx*mi+ri
								oy = rfincy*mj+rj
								ix = mi*somx+si
								iy = mj*somy+sj
								out_reconstruction[rfincy*mj+rj][rfincx*mi+ri] +=\
							  		inp[mj*somy+sj][mi*somx+si] * w[sj][si][rj][ri]
							except IndexError:
								stop = 0
								print "regenerate: index error", str(stop), str(rfincy*mj+rj), str(rfincx*mi+ri)
								raise IndexError
							# dv_y = div(rj, blocky)
							# offset_y = dv_y * spany
							# a = inp[mj*somy+sj][mi*somx+si]
							# b = w[sj][si][rj][ri]
							# out_reconstruction[rfincy*mj+rj+offset_y][rfincx*mi+ri+offset_x] +=\
							#   a * b
							  #inp[mj*somy+sj][mi*somx+si] *\
							  #w[sj][si][rj][ri]

	#out_reconstruction = np.abs(out_reconstruction)
	#out_reconstruction *=255.0/out_reconstruction.max()
	return out_reconstruction

# TODO add span
def generate_top_down(path, wfile, winfo, layer, topdown, mpx, mpy, rfpixelsz):
		# print "maxlayer=" + str(maxlayer)
		# print "topdown[0][0]:"
		# print topdown[0][0]
		# print "mp=" + str(mpx)

		# TODO if maxlayer > 1, also read required files for lower layers
		fileandpath = os.path.join(os.path.expanduser(path), wfile)
		rfsz_x = winfo['C'+str(layer)+'_rf_size_x']
		rfsz_y = winfo['C'+str(layer)+'_rf_size_y']
		rfinc_x = winfo['C'+str(layer)+'_inc_size_x']
		rfinc_y = winfo['C'+str(layer)+'_inc_size_y']

			
		somsz_x = winfo['C'+str(layer)+'_som_size_x']
		somsz_y = winfo['C'+str(layer)+'_som_size_y']
		block_x = winfo['C'+str(layer)+'_block_size_x']
		block_y = winfo['C'+str(layer)+'_block_size_y']
		span_x = winfo['C'+str(layer)+'_span_size_x']
		span_y = winfo['C'+str(layer)+'_span_size_y']
		weights = readweights(fileandpath, rfsz_x, rfsz_y,\
			somsz_x, somsz_y)
		
		#assert(topdown.shape == (somsz_y, somsz_x, rfsz_y, rfsz_x))

		# print 'weights: ' + str(weights.shape)
		# print 'som= ' + str(somsz_x) + ", " + str(somsz_y)
		nextrf = 0
		nextinc = 0
		if layer > 1:
			# count down and go again
			# calculate size rf fields in pixels:
			# rfpix = prev_somsz*rfunits
			# update 2017-09-05: rf sz is correct for span version, but wasnt before 
			#rfsz_x *= winfo['C'+str(maxlayer-1)+'_som_size_x']
			#rfsz_y *= winfo['C'+str(maxlayer-1)+'_som_size_y']
			#rfinc_x *= winfo['C'+str(maxlayer-1)+'_som_size_x']
			#rfinc_y *= winfo['C'+str(maxlayer-1)+'_som_size_y']
			nextrf_x = winfo['C'+str(layer-1)+'_rf_size_x']
			nextrf_y = winfo['C'+str(layer-1)+'_rf_size_y']
			nextinc_x = winfo['C'+str(layer-1)+'_inc_size_x']
			nextinc_y = winfo['C'+str(layer-1)+'_inc_size_y']
			
		#nextweights = readweights(nextfileandpath, nextrf, nextrf,\
		#		nextinc, nextinc, nextsomsz, nextsomsz)	
		regensz_x = rfsz_x # if topdown.shape[1] == somsz_x else rfinc_x*mpx+rfsz_x
		regensz_y = rfsz_y # if topdown.shape[0] == somsz_y else rfinc_y*mpy+rfsz_y

		#if topdown[0][0].shape[1] == somsz_x:
		#	regensz_x = rfsz_x # first time (highest level) regen area == receptive field
		#else:
		#	regensz_x = rfinc_x*mpx+rfsz_x # lower levels: compute area
		#
		#if topdown[0][0].shape[0] == somsz_y:
		#	regensz_y = rfsz_y
		#else: 
		#	regensz_y = rfinc_y*mpy+rfsz_y
		#nextregenweights = np.zeros((nextsomsz, nextsomsz, nextinc*winfo['C'+str(maxlayer)+'_rf_size']+nextrf, nextinc*winfo['C'+str(maxlayer)+'_rf_size']+nextrf))
		topdown_som_x = topdown.shape[1]
		topdown_som_y = topdown.shape[0]
		# regenerated size should be 
		# regenweights = np.zeros((topdown_som_y, topdown_som_x, regensz_y, regensz_x))
		# regenerate top down matrix for this layer
		#for j in xrange(0, topdown_som_y):
		#	for i in xrange(0, topdown_som_x):
				# topdown = np.zeros((somsz, somsz))
				# topdown[j][i] = 1.0
				#weight = weights[j][i]
				#mpx = mpy = 1#winfo['C'+str(maxlayer)+'_rf_size']
				#regenerate(inp, out_x, out_y, mpx, mpy, somx, somy, rfx, rfy, rfincx, rfincy, blockx, blocky, spanx, spany, w):
		#		regenweight = regenerate(topdown[j][i], regensz_x, regensz_y, mpx, mpy, somsz_x, somsz_y,\
		#			rfsz_x, rfsz_y, rfinc_x, rfinc_y, block_x, block_y, span_x, span_y, weights)					
		#		regenweights[j][i] = regenweight
				# mpx = mpy = winfo['C'+str(maxlayer)+'_rf_size']
				# nextregenweight = regenerate(regenweight, nextinc*mpx+nextrf, nextinc*mpx+nextrf, mpx, mpy, nextsomsz, nextsomsz,\
				# 	nextrf, nextrf, nextinc, nextinc, nextweights)
				# nextregenweights[j][i] = nextregenweight
		regenweight = regenerate(topdown, regensz_x, regensz_y, mpx, mpy, somsz_x, somsz_y,\
					rfsz_x, rfsz_y, rfinc_x, rfinc_y, block_x, block_y, span_x, span_y, weights)
		retval = np.zeros((rfpixelsz[0], rfpixelsz[1]))
		if layer > 1:
			
			nextsomsz_x = winfo['C'+str(layer-1)+'_som_size_x']
			nextsomsz_y = winfo['C'+str(layer-1)+'_som_size_y']
			nextblock_x = winfo['C'+str(layer-1)+'_block_size_x']
			nextblock_y = winfo['C'+str(layer-1)+'_block_size_y']
			nextspan_x = winfo['C'+str(layer-1)+'_span_size_x']
			nextspan_y = winfo['C'+str(layer-1)+'_span_size_y']
			nextweightfile = [ f for f in listdir(path)\
				if f[0] != '.' and isfile(join(path,f)) and int(f[1]) == layer-1\
				and check_name(f, layer-1, nextsomsz_x, nextsomsz_y, nextrf_x, nextrf_y, nextinc_x, nextinc_y, nextblock_x, nextblock_y, nextspan_x, nextspan_y, get_input_tag(wfile))]
			#nextfileandpath = os.path.join(os.path.expanduser(path), nextweightfile[0])
			# check_name_span(name, layerix, somx, somy, rfx, rfy, incx, rfincy, blockx, blocky, spanx, spany, inptype):
			nextmap_x = div(winfo['C'+str(layer)+'_rf_size_x'], nextsomsz_x)
			nextmap_y = div(winfo['C'+str(layer)+'_rf_size_y'], nextsomsz_y)
			rfpixelblock = [div(rfpixelsz[0], nextmap_y), div(rfpixelsz[1], nextmap_x)]
			topdownblock = [div(regenweight.shape[0], nextmap_y), div(regenweight.shape[1], nextmap_x)]
			# recursive call
			# have to use actual pixel values here, not in terms of som
			# size
			
			for mj in range(nextmap_y):
				# calculate begin:end values for regenerated img
				aj = mj * rfpixelblock[0]
				bj = aj + rfpixelblock[0]
				td_a_j = mj * topdownblock[0]
				td_b_j = td_a_j + topdownblock[0]
				for mi in range(nextmap_x):
					# calculate begin:end values for regenerated img
					ai = mi * rfpixelblock[1]
					bi = ai + rfpixelblock[1]
					td_a_i = mi * topdownblock[1]
					td_b_i = td_a_i + topdownblock[1]
					# have to do something more complicated here
					retval[aj:bj, ai:bi] = generate_top_down(path, nextweightfile[0], winfo, layer-1,\
						regenweight[td_a_j:td_b_j, td_a_i:td_b_i], mpx=1, mpy=1, rfpixelsz=rfpixelblock)
			#		winfo['C'+str(maxlayer)+'_rf_size_x'],\
			#		winfo['C'+str(maxlayer)+'_rf_size_y'])
		else:
			retval = regenweight
		return retval	
			

def generate_weight_image(somszx, somszy, rfszx, rfszy, w):
	# TODO: add border
	border = (2, 2)
	canvas = (rfszy + 2*border[0], rfszx + 2*border[1])
	weight_image = np.zeros((somszy*canvas[0], \
				somszx*canvas[1]))
	offset = [border[0], border[1]]
	for j in xrange(0, somszy):
		aj = j*(rfszy+2*border[0]) + border[0]
		bj = aj + rfszy
		for i in xrange(0, somszx):
			tmp = np.abs(w[j][i])
			tmp *= 255.0/tmp.max() if tmp.max() > 0.0 else 0.0
			ai = i*(rfszy+2*border[1]) + border[1]
			bi = ai + rfszx
			weight_image[aj:bj, ai:bi] = tmp
			# for jj in xrange(0, rfszy):
			# 	for ii in xrange(0, rfszx):
			# 		jix = j*rfszy + jj 
			# 		iix = i*rfszx + ii 
			# 		weight_image[jix][iix] = tmp[jj][ii]
	return weight_image

def write_image(fname, width, height, data):
	f = open(fname+'.png', 'wb') 
	w = png.Writer(width, \
			height, greyscale=True)
	w.write(f, data)
	f.close()
			
def get_regen_array(winfo, maxlayer):
	# create an 4d array where outer is som size, inner is 
	# total size of receptive field
	# TODO
	rfshape = [0, 0]
	for layer in xrange(1, maxlayer+1):
		rfy = winfo['C'+str(layer)+'_rf_size_y']
		rfx = winfo['C'+str(layer)+'_rf_size_x']
		if layer==1:
			# y
			rfshape[0] = rfy
			rfshape[1] = rfx
		else:
			rfshape[0] *= div(rfy, winfo['C'+str(layer-1)+'_som_size_y'])
			rfshape[1] *= div(rfx, winfo['C'+str(layer-1)+'_som_size_x'])
	somy = winfo['C'+str(maxlayer)+'_som_size_y']
	somx = winfo['C'+str(maxlayer)+'_som_size_x']
	retval = np.zeros((somy, somx, rfshape[0], rfshape[1]))

	return retval

def get_weight_image_array(path, filename, maxlayer):
	wfile = filename
	winfo=parsefilename_span(wfile, maxlayer)
	# print winfo
	# TODO if maxlayer > 1, also read required files for lower layers
	
	somsz_x = winfo['C'+str(maxlayer)+'_som_size_x']
	somsz_y = winfo['C'+str(maxlayer)+'_som_size_y']
	#rf_x = winfo['C'+str(maxlayer)+'_rf_size_x']
	#rf_y = winfo['C'+str(maxlayer)+'_rf_size_y']
	topdown = np.zeros((somsz_y, somsz_x, somsz_y, somsz_x))
	regenweights = get_regen_array(winfo, maxlayer)
	total = somsz_x*somsz_y
	it = 0
	for j in xrange(0, somsz_y):
		for i in xrange(0, somsz_x):
			topdown[j][i][j][i] = 1.0
			tmp = generate_top_down(path, wfile, winfo,\
				maxlayer, topdown[j][i], mpx=1, mpy=1, rfpixelsz=[regenweights.shape[2], regenweights.shape[3]])
			regenweights[j][i] = tmp
			print_progress(iteration=it, total=total, prefix='', suffix='', decimals=1, bar_length=100)
			it += 1
	return regenweights

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
		if f[0] != '.' and isfile(join(path,f)) and int(f[1]) == maxlayer and not (f+".png" in donefiles)]
	print "files to process: " + str(len(weightfiles))
	ctr = 1
	for wfile in weightfiles:
		#fileandpath = os.path.join(os.path.expanduser(path), wfile)
		
		winfo=parsefilename_span(wfile, maxlayer)
		# print winfo
		# TODO if maxlayer > 1, also read required files for lower layers
		
		somsz_x = winfo['C'+str(maxlayer)+'_som_size_x']
		somsz_y = winfo['C'+str(maxlayer)+'_som_size_y']
		#rf_x = winfo['C'+str(maxlayer)+'_rf_size_x']
		#rf_y = winfo['C'+str(maxlayer)+'_rf_size_y']
		topdown = np.zeros((somsz_y, somsz_x, somsz_y, somsz_x))
		regenweights = get_regen_array(winfo, maxlayer)
		total = somsz_x*somsz_y
		it = 0
		for j in xrange(0, somsz_y):
			for i in xrange(0, somsz_x):
				topdown[j][i][j][i] = 1.0
				tmp = generate_top_down(path, wfile, winfo,\
					maxlayer, topdown[j][i], mpx=1, mpy=1, rfpixelsz=[regenweights.shape[2], regenweights.shape[3]])
				regenweights[j][i] = tmp
				print_progress(iteration=it, total=total, prefix='', suffix='', decimals=1, bar_length=100)
				it += 1
				
		#weightimage = generate_weight_image(somsz, somsz, rfsz, rfsz, regenweights)
		# l1somsz_x = winfo['C1_som_size_x']
		# l1somsz_y = winfo['C1_som_size_y']
		# l1inc = winfo['C1_inc_size_x']
		# l1inc = winfo['C1_inc_size_y']
		# l1rf = winfo['C1_rf_size_x']
		# l1rf = winfo['C1_rf_size_y']
		mpsz_x = regenweights[0][0].shape[0] #1 if maxlayer == 1 else winfo['C2_rf_size']
		mpsz_y = regenweights[0][0].shape[1] #1 if maxlayer == 1 else winfo['C2_rf_size']
		weightimage = generate_weight_image(somsz_x, somsz_y, mpsz_x, mpsz_y, regenweights)
		#write_image(wfile, somsz*rfsz, somsz*rfsz, np.nan_to_num(weightimage))
		#write_image(join(imgpath, wfile), somsz_x*mpsz_x, somsz_y*mpsz_y, np.nan_to_num(weightimage))
		write_image(join(imgpath, wfile), weightimage.shape[1], weightimage.shape[0], np.nan_to_num(weightimage))
		print str (ctr) + "/" + str(len(weightfiles)) + " done"
		ctr+=1


if __name__ == '__main__':
	#main(sys.argv[1:])
	#main(["-p/Users/tr1445tj/Code/ikaros/ik-t-tst/Source/UserModules/Models/CSOM-paper/weights/csom", "-l3", "-iweight_images"])
	#print listdir("/Users/tr1445tj/Code/ikaros/ik-t-tst/Source/UserModules/Models/CSOM-paper/weights/tmp")
	main(["-p/Users/tr1445tj/Code/ikaros/ik-t-tst/Source/UserModules/Models/CSOM-paper/weights/tmp", "-l4", "-iweight_images/tmp"])

	# tests:
	#fname = 'C4_CIFAR_C1(rf(3-3)_inc(1-1)_som(12-3)_block(3-3)_span(0-0))C2(rf(36-9)_inc(36-9)_som(20-10)_(block(36-9)_span(24-6))C3(rf(40-20)_inc(40-20)_som(24-12)_block(40-20)_span(100-50))C4(rf(48-24)_inc(48-24)_som(32-16)_block(48-24)_span(264-132)).dat'
	#fname = 'C1_CIFAR_C1(rf(3-3)_inc(1-1)_som(12-3)_block(3-3)_span(0-0)).dat'
	#path = "../weights/tmp/"
	#winfo = parsefilename_span(fname, 4)
	#check_name(name, layerix, somx, somy, rfx, rfy, rfincx, rfincy, blockx, blocky, spanx, spany, inptype):
	#print fname 
	#print check_name(name=fname, layerix=2, somx=20, somy=10, rfx=36, rfy=9, rfincx=36, rfincy=9, blockx=3, blocky=3, spanx=0, spany=0, inptype='CIFAR')
	#print readweights(fileandpath=path+fname, rfszx=3, rfszy=3, somszx=12, somszy=3)

#