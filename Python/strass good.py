#!/usr/bin/python
import csv
from math import log,ceil
from random import choice,seed
from time import time
import numpy

cutoff = 2
seed(99999)

def readmatrix(filename): #CLEAN
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

def pretty(mat): 
	for row in mat:
		print "\t".join(map(str, row)) + '\n'

# Basic Matrix Operations as lambda functions
add = lambda x, y : [[x[i][j] + y[i][j] for j in xrange(len(x))] for i in xrange(len(y))]
sub = lambda x, y : [[x[i][j] - y[i][j] for j in xrange(len(x))] for i in xrange(len(y))]
empty = lambda size: [[0 for _ in xrange(size)] for _ in xrange(size)]
diags = lambda z : [z[i][i] for i in xrange(len(z))]

# def add(A, B):
#     n = len(A)
#     C = [[0 for j in xrange(0, n)] for i in xrange(0, n)]
#     for i in xrange(0, n):
#         for j in xrange(0, n):
#             C[i][j] = A[i][j] + B[i][j]
#     return C

# def sub(A, B):
#     n = len(A)
#     C = [[0 for j in xrange(0, n)] for i in xrange(0, n)]
#     for i in xrange(0, n):
#         for j in xrange(0, n):
#             C[i][j] = A[i][j] - B[i][j]
#     return C

def conventional(X, Y):
	lth = len(X)
	Z = empty(lth)
	for ii in xrange(lth):
		for jj in xrange(lth):
			for kk in xrange(lth):
				Z[ii][jj] += X[ii][kk] * Y[kk][jj]
	return Z

def strasrec(X, Y):
	lth = len(X)
	# If we're at or below the cutoff, switch to the conventional method
	if lth <= cutoff:
		return conventional(X, Y)
	else:
		#print "recurse"
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
		#print 'xs', xs 
		#print 'ys', ys

		# Do all multiplications
		m1 = strasrec(add(xs[0], xs[3]), add(ys[0], ys[3]))
		m2 = strasrec(add(xs[2], xs[3]), ys[0])
		m3 = strasrec(xs[0], sub(ys[1], ys[3]))
		m4 = strasrec(xs[3], sub(ys[2], ys[0]))
		m5 = strasrec(add(xs[0], xs[1]), ys[3])
		m6 = strasrec(sub(xs[2], xs[0]), add(ys[0], ys[1]))
		m7 = strasrec(sub(xs[1], xs[3]), add(ys[2], ys[3]))
		ms = [m1,m2,m3,m4,m5,m6,m7]


		# Calculate Final results
		zs = [add(sub(add(m1, m4), m5), m7), add(m3, m5), add(m2, m4), add(add(sub(m1, m2), m3), m6)]

		# Unite all four matrices
		Z = empty(lth)
		for i in xrange(siz):
			for j in xrange(siz):
				Z[i][j] = zs[0][i][j]
				Z[i][j + siz] = zs[1][i][j]
				Z[i + siz][j] = zs[2][i][j]
				Z[i + siz][j + siz] = zs[3][i][j]
		#print Z
		return Z


def strassen(X, Y):
	n = len(X)
	m = 2**int(ceil(log(n,2)))
	XPrep = empty(m)
	YPrep = empty(m)
	for i in xrange(n):
		for j in xrange(n):
			XPrep[i][j] = X[i][j]
			YPrep[i][j] = Y[i][j]
	ZPrep = strasrec(XPrep, YPrep)
	Z = [[0 for i in xrange(n)] for j in xrange(n)]
	for i in xrange(n):
		for j in xrange(n):
			Z[i][j] = ZPrep[i][j]
	return Z

def generate(dim, size):
	options = range(size+1)
	return [[choice(options) for _ in xrange(dim)] for _ in xrange(dim)]

if __name__ == "__main__":
	X, Y = [], []
	verbose = False
	mode = 'generate'
	size = 10
	checking = True
	if mode == 'generate':
		dim = 40
		X = generate(dim,size)
		Y = generate(dim,size)
	elif mode == 'read':
		X, Y, dim = readmatrix('input.csv')
		print X
		print Y
	start = time()
	#######################
	Z = strassen(X, Y)
	#######################
	end = time()
	if verbose:
		print X
		print Y
		print dim
		pretty(Z)
	
	print "Mat-mult took: " + str(end-start) + ' sec'
	if dim < 500: 
		print diags(Z)
		if checking:
			print "Checking..."
			
			start = time()
			Xnum = numpy.matrix(X)
			Ynum = numpy.matrix(Y)
			W = Xnum * Ynum
			end = time()
			print "\nCorrect from numpy took: " + str(end-start)
	print "\nErrors in diagonal:\n"
	gooddiags = [int(numpy.matrix(Z).diagonal()[:,i]) for i in range(dim)]
	mydiags = diags(Z)
	ct = 0
	for i in range(len(gooddiags)):
		if mydiags[i] != gooddiags[i]:
			ct += 1
	print ct, "total diag elems wrong"
		






