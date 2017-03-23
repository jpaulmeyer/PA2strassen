#!/usr/bin/python
from strass import *

def find_best_cutoff(top_power, dim, size):
	speeddiffs = {}
	for power in range(top_power):
		cutoff = 2**power
		print cutoff
		X = generate(dim,size)
		Y = generate(dim,size)

		start = time()
		Z = strassen(X, Y)
		end = time()
		strasstime = end-start

		start2 = time()
		C = conventional(X, Y)
		end2 = time()
		convtime = end2-start2

		speeddiffs[cutoff] = convtime-strasstime
	print speeddiffs

if __name__ == '__main__':
	top_power = int(argv[1])
	dim = int(argv[2])
	size = int(argv[3])
	find_best_cutoff(top_power, dim, size)