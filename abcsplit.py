''' ABCsplit version 0.9a by 3djake 
----ABOUT-----

A Simple ABC file splitter intended for use with Shroud of the Avatar
ABC files can contain parts for multiple instruments, at the moment this will not work for shroud of the Avatar as 
each instrument must be contained within its own file. This program can do just that and it can be done in batch.
--------------
Note - I have only tested this on Linux nad windows using Python Version 2.7.12
--------------
-----Usage-----
In a terminal or command prompt change to the directory with that contains the abc files to want to work with, a output folder will be created there once the split has been finished.
The program works as follows
python abcsplit.py filename.abc
You can also use wildcards(do multiple files at once) but you have to use qoutes
python abcsplit.py "*.abc"

Windows users, you will have to use the fullpath name to python.

In game, you want to /play songname.txt
Note that we play the txt file not the abc file, you will play the part the instrument you have equipped. If the instrument you are playing does not exist in the txt file then you will not hear anything
---------------
Another Note: The last item of T: in the ABC files must be the name a instrument for example
T: Tomaso Albinon - Adagi (8:21) - Bagpipes
---------------
This program is free software under the the terms of the GNU General Public License as published by
    the Free Software Foundation, Version 3. See <http://www.gnu.org/licenses/>.'''

import sys, getopt, glob, os

lists = []

#Load our file into a list
def loadfile():
	global ourlist
	f = open(filename, "rU")
	ourlist = f.readlines()
	f.close()

#Splits file into sublists
def splitfile():
	global lists
	headerfin = 0
	nl = 0
	sublist = []
	global headerless 
	headerless = 0
	#Check if the file actually has a comment header
	if ourlist [0][0] == "X":
		headerless = 1
	for item in ourlist:
		#Seperate the header, we will need it for each file
		if headerfin == 0 and headerless == 0:
			if item != "\n":
				sublist.append(item)
			else:
				headerfin = 1
				lists.append(sublist)
				sublist = []
		#Count newline characters so we know when to create new list
		if item[0] == "X":
			nl = 0
		if item == "\n":
			nl+=1
		if nl == 2:
			lists.append(sublist)
			sublist = []
		else:
			sublist.append(item)
	#Just in case there was no newline before end of file.
	if ourlist[len(ourlist)-1] != "\n":
		lists.append(sublist)
		sublist = []
	#If there was no header then we need to add a newline so the first instrument gets exported correctly
	if headerless == 1:
		lists[0].insert(0,"\n")
		
	

#Save the files
def exportfile():
	#Crerate a new folder to output new files
	if not os.path.exists("output"):
    		os.makedirs("output")
	i = 1
	if headerless == 1:
		i = 0
	for l in lists[i:]:
		ofile = open("output/" + filename[0:len(filename)-4] + "-" + instname(l) + ".abc", 'w')
		#write the header first
		#Edit as of now, SotA does not play nice with the header comments so we will comment this at for now
		#if headerless == 0:
		#	for line in lists[0]:
		#		ofile.write(line)
		#write the notation for the instrument
		for item in l[1:]:
			ofile.write(item)
		ofile.close()

#Creates the band .txt file
def createbandfile():
	i = 1
	if headerless == 1:
		i = 0
	ofile = open("output/" + filename[0:len(filename)-4] + ".txt", 'w')
	for l in lists[i:]:
		#We will only add instruments currently in the game to this file
		if instname(l) == "Accordian":
			ofile.write("Accordian=" + filename[0:len(filename)-4] + "-" + instname(l) + ".abc\n")
		if instname(l) == "Bagpipes":
			ofile.write("Bagpipes" + filename[0:len(filename)-4] + "-" + instname(l) + ".abc\n")
		if instname(l) == "Drum":
			ofile.write("Drum=" + filename[0:len(filename)-4] + "-" + instname(l) + ".abc\n")
		if instname(l) == "Flute":
			ofile.write("Flute=" + filename[0:len(filename)-4] + "-" + instname(l) + ".abc\n")
		if instname(l) == "Harp":
			ofile.write("Harp=" + filename[0:len(filename)-4] + "-" + instname(l) + ".abc\n")
		if instname(l) == "Lute":
			ofile.write("Lute=" + filename[0:len(filename)-4] + "-" + instname(l) + ".abc\n")
		if instname(l) == "Piano":
			ofile.write("Piano=" + filename[0:len(filename)-4] + "-" + instname(l) + ".abc\n")
		if instname(l) == "StreetOrgan":
			ofile.write("StreetOrgan=" + filename[0:len(filename)-4] + "-" + instname(l) + ".abc\n")
	ofile.close()

#Get instrument name
def instname(l):
	trackinfo = l[2].split('-')
	instrument = trackinfo[len(trackinfo)-1]
	instrument = instrument.strip()
	#Convert from instruments in other games to SotA
	#Add instruments from other games here and what instrument you want to be converted to
	#Make sure you do not end up with duplicate instruments, you may end up with missing parts
	#This part you should customize to your liking
	if instrument == "Basic Lute":
		instrument = "Lute"
	if instrument == "Drums":
		instrument = "Drum"
	if instrument == "Lute of the Ages":
		instrument = "Piano"
	if instrument == "Cello":
		instrument = "Accordian"
	if instrument == "Theorbo":
		instrument = "StreetOrgan"
	if instrument == "Clarinet":
		instrument = "Flute"
	if instrument == "Cowbell":
		instrument = "Drum"
	if instrument == "Pibgorn":
		instrument = "Accordian"
	return instrument

#We will use globbing to enable easy wildcards on multiple platforms
for arg in glob.glob(sys.argv[1]):
	filename = arg
	loadfile()
	splitfile()
	exportfile()
	createbandfile()
	lists = []
