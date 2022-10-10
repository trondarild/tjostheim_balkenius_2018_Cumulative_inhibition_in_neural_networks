import re
import os

# iterate over 3 cols, 8 rows

def processfile(row, col):
	# read file
	filename = 'buf_' + str(row) + '_' + str(col) +'.txt'
	print "filename=" + filename
	if not os.path.isfile(filename):
		print 'file not found'
		return 'file not found'

	fileobj = open(filename, 'r') # open for reading
	

	txt = fileobj.read() # read all lines into a file
	fileobj.close()

	# remove all newlines and handle some special cases
	txt2 = txt.replace('\n','').replace('C2_', ' C2_').replace('-5rand', '-5 rand')

	# find pattern "./ikaros(.+)\.out"
	p = re.compile('\./ikaros(.+?)\.out.+?Stop \(([0-9\.]+) ticks, ([0-9\.]+) s, ')
	lst = p.findall(txt2)
	param_ptrn = re.compile('(\S+?)=([A-Z0-9\.-]*) ')
	headers = list()
	retval = ""
	first = True
	for i in lst:
		# print len(i)
		# parse all parameters, x=y and output
		params = param_ptrn.findall(i[0])
	
		# create a tab-delimited string of everything
		for j in params:
			retval += j[1] + "\t"
			if first:
				headers.append(j[0]) 
		
		retval += i[1] + "\t" + i[2] # ticks + seconds

		retval += "\n"
		first = False

	headers.append("ticks")
	headers.append("seconds")
	return (headers, retval)

if __name__ == '__main__':
	# TODO print headers
	# TODO move to scripts/ and change to allow filenames with path etc (before checking in)
	retval = ""
	headers = ""
	for col in range(3):
		for row in range(8):
			out = processfile(row, col)
			retval += out[1]
			headers = "\t".join(out[0])
			# print out[0]
			# print out[1]
			# print '---'
	retval = headers + "\n" + retval
	fileobj = open("ticks.csv", 'w')
	fileobj.write(retval)
	print retval