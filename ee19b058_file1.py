"""		EE2703 ASSIGNMENT 1
NAME: VINAYAKA SRIDHAR K V V
ROLL NO.: EE19B058
"""
# PYTHON PROGRAM FOR READING A NETLIST AND PRINTING IN THE REVERSE ORDER

from sys import argv, exit	#importing module sys
pycode = argv[0]

CIRCUIT = '.circuit' # defining the constants
END = '.end'
""" Sanity Check whether there is a input file given or not"""
if len(argv) != 2:
	#if the there is no input file mentioned and print the usage method
	print("\nPlease give a input file: Usage: %s <input file name>" % pycode)
	exit()
	
filename = argv[1]		# Calling the argument after the python file in the commandline as the filename
try:
	with open(filename) as f:		#Taking the input file as f
	#Initialising values of start and end
		start=1
		end=0
		lines = f.readlines()		#reading the input file line by line and storing them in the list "lines" 
		for line in lines:
			word = line.split()	# Checking if there is line starting with .circuit
			if word[0]==CIRCUIT:	# if there is a line starting with .circuit then make its index as start
				start = lines.index(line)
		
			if word[0]==END:	# Checking if there is line starting with .end
				end = lines.index(line)	# if yes then make its index as end
				
		""" Sanity check: whether input file has valid circuit defintion 
			that is whether its starts with .circuit and ends with .end"""
		if start >= end:
			print("Invalid Circuit Definition")	#if the file fails to comply with the circuit defintion then print out error statement
			exit(0)
			
#printing the lines in the reverse order
	for i in range(end-1,start,-1):
		tokens = lines[i].split("#")[0].split()     #removing the comments and splitting the lines into words and calling them tokens
		print(" ".join(reversed(tokens)))           #printing the tokens in reverse order	

# if no file exists with the name given by the user
#then issue an IOError saying invalid file
except IOError:
	print("Invalid File")
	exit(0)
