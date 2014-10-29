
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

# open the temp.txt file
# file = open(temp, "r")
#line = file.readline()
# list = [];
#for line in file:
#	list.append(line)
#	print '> Date: ' + line[15:31] #date
#	print '> RA: ' + line[32:43] #ra
#	print '> Dec: ' + line[44:55] #dec
#	print '> Mag: ' + line[65:70] #magnitude
#	print '> Observatory Code: ' + line[77:80] + '\n' #observatory code
# file.close()	

# runs ./fo (Find_Orb) on the stuff file
stuff = 'temp.txt'
print '--------------- Begin Find_Orb ----------------'
subprocess.call(["./fo", stuff])
print '----------------- End Find_Orb-----------------'

# open the result of Find_Orb
# elements = open("elements.txt", "r")
# line = elements.readlines()
# print '\n\n--------------- Begin elements.txt ----------------'
# lines 23 and 24
# print line[23]
# print line[24]
# print '--------------- End elements.txt ------------------'
# elements.close()

# open the mpc_format
mpc = open("mpc_fmt.txt", "r")
stuff = mpc.readline()
print '\n\n--------------- Begin mpc_fmt.txt ----------------'
print stuff
print '--------------- End mpc_fmt.txt ------------------\n'
mpc.close()

a = float(stuff[92:103]);
i = float(stuff[59:68]);
e = float(stuff[70:79]);

print 'a = ' + str(a)
print 'i = ' + str(i)  
print 'e = ' + str(e)

# CONVERT TO RADIANS OR ELSE YOU GET ABSURDLY HIGH NUMBERS
i = math.radians(i);

delta_v = cdv_SH(a,e,i);

if str(delta_v) == "nan":
	print "\nNo Delta-v computed :(\n" 
else:
	print '\nDelta-v: ' + str(delta_v) + ' km/s\n'	

#print '\nRemoving temporary files...'
os.remove('temp.txt') 
#print 'Removed!\n'