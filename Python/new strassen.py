#!/usr/bin/env python
import csv

def readmatrix(filename):
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

def conv(x, y, dim, nice=False):


dim = 8
one = [[1 for _ in range(dim)] for _ in range(dim)]
two = [[1 for _ in range(dim)] for _ in range(dim)]

if __name__ == '__main__':
	conv(one, two, dim)