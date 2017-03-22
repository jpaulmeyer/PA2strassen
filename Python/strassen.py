#!/usr/bin/env python

import numpy as np
import csv
import math
# class Matrix(object):

# 	def __init__(self, a, b, c, d): #Where a,b,c,d are matrices
# 		self.comps = [a,b,c,d]

# 	def __getitem__(self, i):
# 		return self.comps[i]

def addmat(mat1, mat2):
	flatten = lambda l : [item for sublist in l for item in sublist]
	if len(mat1) == len(mat2) and type(mat1[0]) == int:
		out = [mat1[i] + mat2[i] for i in range(len(mat1))]
		return out
	else:
		



def conv(x, y, dim, nice=False):
	#print dim
	print '\n'
	#print 'x', x, type(x)
	#print 'y', y, type(y)
	if dim <= 2:
		if dim < 2: 
			raise "Dim Error (me)"
		tl = x[0]*y[0] + x[1]*y[2]
		tr = x[0]*y[1] + x[1]*y[3]
		bl = x[2]*y[0] + x[3]*y[2]
		br = x[2]*y[1] + x[3]*y[3]
		out = [tl,tr,bl,br]
		#print 'ans', out
		return out
	else:
		tl = addmat(conv(x[0],y[0], dim/2), conv(x[1],y[2], dim/2))
		tr = addmat(conv(x[0],y[1], dim/2), conv(x[1],y[3], dim/2))
		bl = addmat(conv(x[2],y[0], dim/2), conv(x[3],y[2], dim/2))
		br = addmat(conv(x[2],y[1], dim/2), conv(x[3],y[3], dim/2))
		#print tl
		#print tr
		#print bl
		#print br
		out = [tl,tr,bl,br]
		#for elem in out: 
		#	print 'ans', elem
		return out
# if nice:
# 	nicemat([[tl,tr],[bl,br]])
# 	return [[tl,tr],[bl,br]]
# else:


def generate(dim):
	flatten = lambda l : [item for sublist in l for item in sublist]
	return flatten(np.random.randint(2, size=(dim, dim)).tolist())

def read_input(filename='input.csv'):
	out = []
	with open(filename, 'rU') as fil:
		reader = csv.reader(fil)
		for row in reader:
			out.append(int(row[0]))
	lth = len(out)
	dim = math.log(lth/2, 2)
	x = out[:lth/2]
	y = out[lth/2:]
	return x, y, dim

if __name__ == '__main__':
	###################
	mode = 'hard' # read, generate, hard
	###################
	if mode == 'generate':
		dim = 4   #2**2
		print dim
		x = generate(dim)
		y = generate(dim)
		print 'xtest', x
		print 'ytest', y
		print conv(x, y , dim , False)
	elif mode == 'read':
		x, y, dim = read_input()
		print dim
		print 'xtest', x
		print 'ytest', y
		print conv(x, y, dim , False)
	elif mode == 'hard':
		

		dim = 8


		if dim == 8:
			print conv([[[1,2,3,4],[5,6,7,8],[9,10,11,12],[13,14,15,16]],[[1,2,3,4],[5,6,7,8],[9,10,11,12],[13,14,15,16]],\
				[[0,1,1,0],[1,0,1,1],[2,1,0,1],[4,3,2,1]],[[0,1,1,0],[1,0,1,1],[2,1,0,1],[4,3,2,1]]],[[[0,1,1,0],\
				[1,0,1,1],[2,1,0,1],[4,3,2,1]],[[0,1,1,0],[1,0,1,1],[2,1,0,1],[4,3,2,1]],[[0,1,1,0],[1,0,1,1],\
				[2,1,0,1],[4,3,2,1]],[[0,1,1,0],[1,0,1,1],[2,1,0,1],[4,3,2,1]]],
				8 #dim
				)
		if dim == 4:
			print conv(
				[[1,2,3,4],[5,6,7,8],[9,10,11,12],[13,14,15,16]],
				[[0,1,1,0],[1,0,1,1],[2,1,0,1],[4,3,2,1]],
				4 #dim
				)
		if dim == 2:
			print conv(
				[1,2,3,4],
				[5,6,7,8],
				2 #dim
				)


	########### THESE ARE BOTH RETURNING MATRICES OF THE FORM [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16]











############################
#        ARCHIVE           #
############################


# def nicemat(mat):
# 	out = ''
# 	out += '[\n\t' + str(mat[0][0]) + ', '
# 	out += str(mat[0][1]) + '\n\t'
# 	out += str(mat[1][0]) + ', '
# 	out += str(mat[1][1]) + '\n]'
# 	print out





def conventional_single(x, y, dim,nice=False):	
	if dim in [0,1,2,4,8,16]:
		tl = x[0][0]*y[0][0] + x[0][1]*y[1][0]
		tr = x[0][0]*y[0][1] + x[0][1]*y[1][1]
		bl = x[1][0]*y[0][0] + x[1][1]*y[1][0]
		br = x[1][0]*y[0][1] + x[1][1]*y[1][1]
	if nice:
		nicemat([[tl,tr],[bl,br]])
		return [[tl,tr],[bl,br]]
	else:
		return [[tl,tr],[bl,br]]




