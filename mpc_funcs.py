def mpc_connect(str):

	"""
	Connect to the Minor Planet Center. 
	Download specified asteroid's .dat file into .txt file.
	"""

	import urllib
	import urllib2

	query_args = { 'object_id':str} 
	init_ast = urllib.urlencode(query_args);
	data_ast = str.replace(" ","_");

	print '\nRetrieving dataset for ' + str + ' from Minor Planet Center...' + '\n'

	# use url to initialize url (tricks mpc to thinking we are not software)
	s_url = 'http://www.minorplanetcenter.net/db_search/show_object?';
	initurl = s_url + init_ast;
	init = urllib2.urlopen(initurl);

	# validation of code
	# print "This gets the code: ", init.code
	# print "This gets the code: ", data.code

	# after initialization, get data
	tmp = 'http://www.minorplanetcenter.net/tmp/'
	dataurl = tmp + data_ast + '.dat';
	data = urllib2.urlopen(dataurl)


	# transfer data from .dat to temp.txt file
	temp = "temp.txt";
	dl = open(temp, "w")
	dl.write(data.read())
	dl.close()

def findorb(file):
	"""
	Run Find_Orb (./fo) on a text file
	Find_Orb software MUST be located in same directory
	"""

	import subprocess

	print '--------------- Begin Find_Orb ----------------'
	subprocess.call(["./fo", file])
	print '----------------- End Find_Orb-----------------'