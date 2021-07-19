"""		EE2703 ASSIGNMENT 2
NAME: VINAYAKA SRIDHAR K V V
ROLL NO.: EE19B058
"""
# PYTHON PROGRAM FOR READING A NETLIST AND ANALYSING IT AND SOLVING FOR NODE VOLTAGES
#		USING MODIFIED NODAL ANALYSIS

from sys import argv, exit	#importing module sys
pycode = argv[0]

CIRCUIT = '.circuit' # defining the constants
END = '.end'
AC = '.ac'
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
	"""for i in range(start+1,end):
		tokens = lines[i].split("#")[0].split()     #removing the comments and splitting the lines into words and calling them tokens
		print(" ".join(reversed(tokens)))           #printing the tokens in reverse order	"""

	import numpy as np
	#defining cosine and sine functions for easy use later
	cos=np.cos
	sin=np.sin
	#assigning pi value
	pi=np.pi
	node=np.array(range(0,2*(end-1)))	#creating a node array to store the from and to nodes of circuit elements
	for k in range(2*(end-1)):
		node[k]=0
	w=0
	nor=0
	nol=0
	noc=0
	nov=0	#nov is the variable for number of voltage sources to keep track of how many current variables should be considered through them
	k=0
	for i in range(start+1,end):
		tokens = lines[i].split("#")[0].split()
		#initialising the string GND as an integer 0 for further convenience
		if tokens[1]=="GND":
			tokens[1]=0
		if tokens[2]=="GND":
			tokens[2]=0
		#sir/madam some more time required to implement capacitors and inductors and ac sources
		if tokens[0]!= AC:
			#'from' node and 'to' node assigned to x,y respectively
			x=int(tokens[1])-1
			y=int(tokens[2])-1
			#if the from node and to node are given same then issue an error statement
			if x==y:
				print("error: invalid connection of circuit element %s" % tokens[0])
				exit(0)
			#giving input values of node array
			node[k]=int(tokens[1])
			k=k+1
			node[k]=int(tokens[2])
			k=k+1
		#counting the number of resistors
		if tokens[0][0] == "R":
			nor=nor+1
		#counting the number of inductors
		if tokens[0][0] == "L":
			nol=nol+1
		#counting the number of capacitors
		if tokens[0][0] == "C":
			noc=noc+1
		#counting the number of volatge sources
		if tokens[0][0] == "V":
			nov=nov+1
		if tokens[0][0] == "V":
			n=int(tokens[0][1])
			vindex=np.array(range(nov)) #storing the indices of the lines defining voltage sources for future use
			vindex[n-1]=i
		#if there is an ac source then take in the frequency and compute the angular frequency
		if tokens[0] == AC:
			f=float(tokens[2])
			w=2*pi*f
			
	print(node)
#Finding the number of nodes in the given circuit
	nmax=node[0]
	for z in range(0,len(node)):
		if node[z]>nmax:
			nmax=node[z]
	#printing some useful values computed above about the circuit
	print("number of nodes =",nmax)
	print("number of voltage sources=",nov)
	print("number of inductors =",nol)
	print("number of capacitors =",noc)
	#if all the voltage sources are ac then make nol=0 because in dc analysis of inductor only we model it as a 0v voltage source and a separate equation is needed but in ac analysis separate equation is not needed as inductor will be converted to an impedence in frequency domain
	for vind in vindex: 
		if lines[vind].split("#")[0].split()[3] == "ac": 
			nol=0
	# m is the total number of linear equations and number of unknown variables
	m=nmax+nol+nov
	
	print("number of unknown voltages and currents=",m)
	#initialising the admittance and the current or constant matrix with zeros
	G=np.zeros([m,m],dtype=complex)
	I=np.zeros([m,1],dtype=complex)
	
	#Traversing the file again and analysing the circuit in it
	for i in range(start+1,end):
		tokens = lines[i].split("#")[0].split()
		# making GND as 0 for convenience
		if tokens[1]=="GND":
			tokens[1]=0
		if tokens[2]=="GND":
			tokens[2]=0
		#creating the admittance stamps of each resistor in the circuit
		if tokens[0][0] == "R":
			x=int(tokens[1])-1
			y=int(tokens[2])-1
			#stamp if the resistor is connected between two nodes other than ground
			if x!=y and x!=-1 and y!=-1:
				G[x][x] = G[x][x] + float(tokens[3])**(-1)
				G[x][y] = G[x][y] - float(tokens[3])**(-1)
				G[y][x] = G[y][x] - float(tokens[3])**(-1)
				G[y][y] = G[y][y] + float(tokens[3])**(-1)
			#stamp if the from node is ground
			if x==-1:
				G[y][y] = G[y][y] + float(tokens[3])**(-1)
			#stamp if the to node is ground
			if y==-1:
				G[x][x] = G[x][x] + float(tokens[3])**(-1)
		
		#creating the stamp of each voltage source in the circuit		
		if tokens[0][0] == "V":
			n=int(tokens[0].split("V")[1])
			x=int(tokens[1])-1
			y=int(tokens[2])-1
			vindex[n-1]=i
			
			#if the voltage source is an ac source then compute peak voltage and the phase
			if tokens[3]=="ac":
				nol=0
				phi=float(tokens[5])*pi/180
				Vp=float(tokens[4])*0.5
				
				I[nmax+nol+n-1][0]=I[nmax+nol+n-1][0]+(Vp*(cos(phi)+sin(phi)*1j))
			if x!=-1:
				#if the to node is ground
				G[x][nmax+nol+n-1]=G[x][nmax+nol+n-1]-1
				G[nmax+nol+n-1][x]=G[nmax+nol+n-1][x]+1
				#stamp if neither from node nor to node is ground
				if y!=-1:
					G[y][nmax+nol+n-1]=G[y][nmax+nol+n-1]+1
					G[nmax+nol+n-1][y]=G[nmax+nol+n-1][y]-1
			#stamp if the from node is ground
			if x==-1:
				G[y][nmax+n-1]=G[y][nmax+n-1]+1
				G[nmax+n-1][y]=G[nmax+n-1][y]-1
			
			if tokens[3]!="dc" and tokens[3]!="ac" and tokens[3]==tokens[-1]:
				#inputting corresponding value of the voltage source in the constant matrix		
				I[nmax+nol+n-1][0]=I[nmax+nol+n-1][0]+float(tokens[3])
			if tokens[3]=="dc":
				I[nmax+nol+n-1][0]=I[nmax+nol+n-1][0]+float(tokens[4])
			
		#creating the stamps for current sources
		if tokens[0][0] == "I":
			x=int(tokens[1])-1
			y=int(tokens[2])-1
			#if neither from node nor to node is ground
			#then the corresponding stamp
			if tokens[3]!="dc" and tokens[3]!="ac" and tokens[3]==tokens[-1]:
				if x!=-1 and y!=-1:
					I[x][0]=I[x][0]-float(tokens[3])
					I[y][0]=I[y][0]+float(tokens[3])
				#if the from node is ground then the corresponding stamp
				if x==-1:
					I[y][0]=I[y][0]+float(tokens[3])
				#if the to node is ground then the corresponding stamp
				if y==-1:
					I[x][0]=I[x][0]-float(tokens[3])
			if tokens[3]=="dc":
				if x!=-1 and y!=-1:
					I[x][0]=I[x][0]-float(tokens[4])
					I[y][0]=I[y][0]+float(tokens[4])
				#if the from node is ground then the corresponding stamp
				if x==-1:
					I[y][0]=I[y][0]+float(tokens[4])
				#if the to node is ground then the corresponding stamp
				if y==-1:
					I[x][0]=I[x][0]-float(tokens[4])
					
			if tokens[3]=="ac":
				phi=float(tokens[5])*pi/180
				if x!=-1 and y!=-1:
					I[x][0]=I[x][0]-((float(tokens[4])/2)(cos(phi)+sin(phi)*1j))
					I[y][0]=I[y][0]+((float(tokens[4])/2)(cos(phi)+sin(phi)*1j))
				#if the from node is ground then the corresponding stamp
				if x==-1:
					I[y][0]=I[y][0]+((float(tokens[4])/2)(cos(phi)+sin(phi)*1j))
				#if the to node is ground then the corresponding stamp
				if y==-1:
					I[x][0]=I[x][0]-((float(tokens[4])/2)(cos(phi)+sin(phi)*1j))
					
		if tokens[0][0]=="C":
			x=int(tokens[1])-1
			y=int(tokens[2])-1
			C=float(tokens[3])
				#if the source is dc then do nothing as it will be considered as open citcuit
				#do nothing
			for vind in vindex: 
				if lines[vind].split("#")[0].split()[3] == "ac":
					if x!=y and x!=-1 and y!=-1:
						G[x][x] = G[x][x] + C*(w)*1j
						G[x][y] = G[x][y] - C*(w)*1j
						G[y][x] = G[y][x] - C*(w)*1j
						G[y][y] = G[y][y] + C*(w)*1j
					#stamp if the from node is ground
					if x==-1:
						G[y][y] = G[y][y] + C*(w)*1j
					#stamp if the to node is ground
					if y==-1:
						G[x][x] = G[x][x] + C*(w)*1j
					
		if tokens[0][0]=="L":
			x=int(tokens[1])-1
			y=int(tokens[2])-1
			#checking whether all the sources are dc or not
			for vind in vindex: 
				if lines[vind].split("#")[0].split()[3] == "dc" or lines[vind].split("#")[0].split()[3] == lines[vind].split("#")[0].split()[-1]:
					n=int(tokens[0].split("L")[1])
					print(n)
					if x!=-1:
						#if the to node is ground
						G[x][nmax+n-1]=G[x][nmax+n-1]-1
						G[nmax+n-1][x]=G[nmax+n-1][x]+1
						#stamp if neither from node nor to node is ground
						if y!=-1:
							G[y][nmax+n-1]=G[y][nmax+n-1]+1
							G[nmax+n-1][y]=G[nmax+n-1][y]-1
					#stamp if the from node is ground
					if x==-1:
						G[y][nmax+n-1]=G[y][nmax+n-1]-1
						G[nmax+n-1][y]=G[nmax+n-1][y]+1
 
				#in case the source is ac
				if lines[vind].split("#")[0].split()[3] == "ac":
					 if x!=y and x!=-1 and y!=-1:
					 	G[x][x] = G[x][x] -((float(tokens[3])*w)**(-1))*1j
					 	G[x][y] = G[x][y] +((float(tokens[3])*w)**(-1))*1j
					 	G[y][x] = G[y][x] +((float(tokens[3])*w)**(-1))*1j
					 	G[y][y] = G[y][y] -((float(tokens[3])*w)**(-1))*1j
					 
					 #stamp if the from node is ground	
					 if x==-1:
					 	G[y][y] = G[y][y] -((float(tokens[3])*w)**(-1))*1j
					 
					 #stamp if the to node is ground	
					 if y==-1:
					 	G[x][x] = G[x][x] -((float(tokens[3])*w)**(-1))*1j
	
	#Printing the above created admittance matrix and the constant matrix
	print("\nThe admittance matrix\n",G)
	print("\nThe constant matrix\n",I)
	
	#SOLVING THE ADMITTANCE MATRIX AND CONSTANT MATRIX TO GET THE VARIABLE MATRIX OR ARRAY
	#  [G]*[V] = [I] here we know the [G] matrix and the [I] matrix we have to solve for [V] matrix
	V=np.linalg.solve(G,I)
	
	#Printing the solution matrix or the variable matrix
	print("\nThe variable matrix or the solution\n",V,"\n")
	
	import cmath
	for a in range(0,nmax):
		v=cmath.polar(V[a])[0]
		phase=cmath.polar(V[a])[1]*180/pi
		print("The voltage at node",a+1," = %.10f"% v,"Cos(%.10f"% w,"t+",phase,") V")
	for b in range(0,nov):
		I=cmath.polar(V[nmax+b])[0]
		phase=cmath.polar(V[nmax+b])[1]*180/pi
		print("The current through V",b+1," = %.10f"% I,"Cos(%.10f"% w,"t+",phase,") A")
# if no file exists with the name given by the user
#then issue an IOError saying invalid file
except IOError:
	print("Invalid File")
	exit(0)
