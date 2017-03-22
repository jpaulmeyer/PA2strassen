#!/usr/bin/python

a = [1,2,3,4,5,6,7,8,9,1,2,3,4,5,6,7]
b = [4,5,6,7,8,9,1,2,3,7,6,5,4,3,2,1]
dim = 4

out = [a[i:i+dim] for i in range(0, len(a), dim)]

print out