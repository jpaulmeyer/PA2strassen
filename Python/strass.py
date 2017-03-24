#!/usr/bin/python

# Harvard ID 40939695
# Quick intro: Hi! I've completed the programming assignment, and while it's a bit slow in real-time speed,
# the modified Strassen algorithm *********



import csv # For file IO
from math import log,ceil # Log and ceil for determining padding etc.
from random import choice,seed # Seed for consistent results (testing) and use choice for random nums
from time import time # For timing how long things take
from sys import argv # For command line args
import cProfile

cutoff = 16 # Cutoff of when to switch to strassen
seed(99999) # Seeding random number generator for consistency
size = 1 # How large of positive or negative numbers should be allowed in the array
print "Cutoff", cutoff, '\n'
usagestring = "Usage: ./strassen flag dimension inputfile | any extras into list"
modestring = "Mode not included, use 0, 1, 2 for read, generate, hard"
modes_by_index = ['read', 'generate', 'hard', 'verbose', 'testing'] #Graders will be using the read mode

#Flags: sets mode argument
#### 0: read (from inputfile) ***normal for graders)
#### 1: generate (makes matrices from seed)
#### 2: hard input (not implemented yet)
#### 3: verbose (prints a lot, submode of generate)
#### 4: testing things

def generate(dim, size):
	options = range(size+1)
	return [[choice(options) for _ in xrange(dim)] for _ in xrange(dim)]

# Basic Matrix Operations as lambda functions
add = lambda x, y : [[x[i][j] + y[i][j] for j in xrange(len(x))] for i in xrange(len(y))]
sub = lambda x, y : [[x[i][j] - y[i][j] for j in xrange(len(x))] for i in xrange(len(y))]
empty = lambda size: [[0 for _ in xrange(size)] for _ in xrange(size)]
diags = lambda z : [z[i][i] for i in xrange(len(z))]

def conventional1(X, Y):
	lth = len(X)
	Z = empty(lth)
	for ii in xrange(lth):
		for jj in xrange(lth):
			for kk in xrange(lth):
				Z[ii][jj] += X[ii][kk] * Y[kk][jj]
	return Z

def conventional2(X, Y): # Switching the two kk and jj loops makes it a bit faster
	lth = len(X)
	Z = empty(lth)
	for ii in xrange(lth):
		for kk in xrange(lth):
			for jj in xrange(lth):
				Z[ii][jj] += X[ii][kk] * Y[kk][jj]
	return Z

def strasrec(X, Y):
	lth = len(X)
	# If we're at or below the cutoff, switch to the conventional2 method
	if lth <= cutoff:
		return conventional2(X, Y)
	else:
		# Tee up the four submatrices, wrapped up as x's and y's (xs,ys). Dividing dimension by 2 each time.
		siz = lth/2
		xs = [empty(siz) for _ in xrange(4)]
		ys = [empty(siz) for _ in xrange(4)]

		# Divide into four matrices 
		for i in xrange(siz):
			for j in xrange(siz):
				# X submatrices: top left, top right, bot left, bot right
				xs[0][i][j] = X[i][j]
				xs[1][i][j] = X[i][j + siz]
				xs[2][i][j] = X[i + siz][j]
				xs[3][i][j] = X[i + siz][j + siz]
				# Y submatrices: top left, top right, bot left, bot right
				ys[0][i][j] = Y[i][j] 
				ys[1][i][j] = Y[i][j + siz]
				ys[2][i][j] = Y[i + siz][j]
				ys[3][i][j] = Y[i + siz][j + siz]

		# Do all multiplications
		m1 = strasrec(add(xs[0], xs[3]), add(ys[0], ys[3]))
		m2 = strasrec(add(xs[2], xs[3]), ys[0])
		m3 = strasrec(xs[0], sub(ys[1], ys[3]))
		m4 = strasrec(xs[3], sub(ys[2], ys[0]))
		m5 = strasrec(add(xs[0], xs[1]), ys[3])
		m6 = strasrec(sub(xs[2], xs[0]), add(ys[0], ys[1]))
		m7 = strasrec(sub(xs[1], xs[3]), add(ys[2], ys[3]))
		
		ms = [m1,m2,m3,m4,m5,m6,m7]


		# Calculate Final results (top left, top right, bot left, bot right)
		zs = [ add(sub(add(m1, m4), m5), m7),     add(m3, m5), \
		\
			   add(m2, m4),        add(add(sub(m1, m2), m3), m6) ]

		# Unite all four matrices
		Z = empty(lth)
		for i in xrange(siz):
			for j in xrange(siz):
				Z[i][j] = zs[0][i][j] # Top left
				Z[i][j + siz] = zs[1][i][j] # Top right
				Z[i + siz][j] = zs[2][i][j] # Bot left
				Z[i + siz][j + siz] = zs[3][i][j] # Bot right

		# Return the completed matrix
		return Z

def pad(X, Y, lth):
	powertwo = 2**int(ceil(log(lth,2)))
	padX, padY = empty(powertwo), empty(powertwo)
	for i in xrange(lth):
		for j in xrange(lth):
			padX[i][j] = X[i][j]
			padY[i][j] = Y[i][j]
	return padX, padY

def unpad(padZ, lth):
	Z = empty(lth)
	for i in xrange(lth):
		for j in xrange(lth):
			Z[i][j] = padZ[i][j]
	return Z

def strassen(X, Y): # Pad, multiply, unpad (won't pad if perfect power of two)
	# Pad X and Y with zeros up to next power of two, regardless of if odd or even
	lth = len(X)
	padX, padY = pad(X, Y, lth)
	# Multiply the padded matrices
	padZ = strasrec(padX, padY)
	# Unpad resulting padded matrix padZ
	Z = unpad(padZ, lth)
	return Z
	
def readmatrix(filename): #CLEAN
	if filename != None:
		out = []
		with open(filename, 'rU') as fil:
			reader = csv.reader(fil)
			for row in reader:
				out.append(int(row[0]))
		lth = len(out)
		dim = int(log(lth/2, 2))
		x = out[:lth/2]
		y = out[lth/2:]
		xout = [x[i:i+dim] for i in xrange(0, len(x), dim)]
		yout = [y[i:i+dim] for i in xrange(0, len(y), dim)]
		return xout, yout, int(dim)
	else:
		print "Messed up filename"

def verify(X, Y, Z): # Make sure X * Y = Z via numpy (only used for checking purposes)
	import numpy
	U = numpy.matrix(X)
	V = numpy.matrix(Y)
	start2 = time()
	W = U * V
	end2 = time()
	print "Numpy took: " + str(end2-start2) + ' sec' # Report timing of Numpy version
	gooddiags = [int(W.diagonal()[:,i]) for i in range(dim)]
	mydiags = diags(Z)
	ct = 0
	for i in range(len(gooddiags)):
		if mydiags[i] != gooddiags[i]:
			ct += 1
	print "Total errors: ", ct
	return mydiags == gooddiags

def do_tests(dim, times):
	import numpy
	adds1, subs1, adds2, subs2 = [],[],[],[]
	for _ in xrange(times):
		aa = generate(dim, size)
		bb = generate(dim, size)
		start = time()
		D = strassen(aa,bb)
		mid = time()
		# E = add(aa,bb)
		# end = time()
		start2 = time()
		F = conventional2(aa,bb)
		mid2 = time()
		# G = sub(aa,bb)
		# end2 = time()
		adds1.append(mid-start)
		# adds2.append(end-mid)
		adds2.append(mid2-start2)
		# subs2.append(end2-mid2)
	avg1 = sum(adds1)#/len(adds1)
	avg2 = sum(adds2)#/len(adds2)
	# avg3 = sum(subs1)#/len(subs1)
	# avg4 = sum(subs2)#/len(subs2)
	print "On avg..."
	print "Conventional1 took: " + str(avg1) + ' sec'
	print "Conventional2 took: " + str(avg2) + ' sec' 
	# print "My sub took: " + str(avg3) + ' sec'
	# print "Numpy sub took: " + str(avg4) + ' sec' 

def main(mode, dim, inputfile=None, checking=False):
	X, Y = [], []
	print mode
	# Act based on mode given through argv
	if mode not in modes_by_index:
		print modestring
	elif mode == 'read':
		print mode
		X, Y, dim = readmatrix(inputfile)
	elif mode == 'generate':
		X = generate(dim,size)
		Y = generate(dim,size)
	elif mode == 'verbose':
		pass
	elif mode == 'testing':
		do_tests(35, 50)
		return

	### In all cases, take in X and Y (list of lists)...
	start = time()
	Z = strassen(X, Y)	# Strassen multiply them, converting to conventional whenever you want
	end = time()
	print "Strassen took: " + str(end-start) + ' sec' # Report timing of my Strassen implementation
	if dim < 300:
		print diags(Z)

	start2 = time()
	C = conventional2(X, Y)
	end2 = time()
	convtime = end2-start2
	print "Conventional took: " + str(end2-start2) + ' sec' # Report timing of my Strassen implementation
	if dim < 300:
		print diags(C)

	if checking:
		print "Checking... " + str(verify(X, Y, Z))

# Only when running my program from the command line, do the following
if __name__ == "__main__":
	# Argv parsing/checking
	arg_len = len(argv)

	if arg_len <= 2: # Not enough arguments
		print usagestring + "\n" + "Need more arguments"
	elif int(argv[1]) > len(modes_by_index): # Make sure mode is within range
		print modestring
	elif arg_len == 3: # 
		mode, dim = modes_by_index[int(argv[1])], int(argv[2])
	 	main(mode, dim, checking=True)
	elif arg_len == 4:
		mode, dim = modes_by_index[int(argv[1])], int(argv[2])
		inputfile = str(argv[3])
		main(mode, dim, inputfile)
	elif arg_len >= 5:
		extras = argv[4:]
		print usagestring + "\n" + "You used extra arguments {}".format(extras)


