
# -*- coding: utf-8 -*-
# 
# Pulls data from Minor Planet Center databases
#
# Uses Find_Orb software from Project Pluto 
# http://www.projectpluto.com/find_orb.htm
# 
# -*- -*- -*- -*- -*- -*- -*- -*- -*- -*- -*- -*- #

import sys
import os
import math
import urllib
import urllib2
import subprocess

# import delta_v functions
from computedeltav import cdv_SH, cdv_SH_bennerbug
from mpc_funcs import findorb

# input asteroid
ast = raw_input("Enter Asteroid Name: ")
query_args = { 'object_id':ast} 
init_ast = urllib.urlencode(query_args);
data_ast = ast.replace(" ","_");

#what = cdv_SH(a,e,i);

# Connect to and download asteroid's .dat file
print '\nRetrieving dataset for ' + ast + ' from Minor Planet Center...' + '\n'

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

# open storage files
a_file = open("a.txt","w");
i_file = open("i.txt","w");
e_file = open("e.txt","w");
delta_v_file = open("delta_v.txt","w");


row = "row.txt"
rw = open(row, "w")
rw.close()

rw = open(row, "a")

with open(temp, "r") as file:
  for line in file:
	print line	
  	rw.write(line)
	subprocess.call(["./fo", "row.txt"])
	
	if os.path.isfile("mpc_fmt.txt") == "TRUE":
		# open the mpc_format
		mpc = open("mpc_fmt.txt", "r")
		stuff = mpc.readline()
	

		# get parameters
		a = float(stuff[92:103]);
		i = float(stuff[59:68]);
		e = float(stuff[70:79]);

		# convert i to radians
		i = math.radians(i);

		# get delta_v
		delta_v = cdv_SH(a,e,i);

		#write everything
		a_file.write(str(a) + "\n")
		i_file.write(str(i) + "\n")
		e_file.write(str(e) + "\n")
		delta_v_file.write(str(delta_v) + "\n")

rw.close()
#print '\nRemoving temporary files...'
#os.remove('temp.txt') 
#print 'Removed!\n'