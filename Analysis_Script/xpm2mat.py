#!/usr/bin/python

import sys

f = open(sys.argv[1], 'r')
fw =  open(sys.argv[2], 'w')

fw.write("#This file is created by xpm2mat program that converts a file with xpm format to a 3xn matrix that can be plotted by 3D plotting progtams such as gnuplot.\n#First reaction coordinate\tsecond reaction coordinate\tGibbs Free Energy")


nline=0
ener=[]
ener_l=[]
ticks=[]
lz=0
start_line = 1000000000
for line in f:
	nline = nline + 1
	if nline <= (lz + start_line) and nline > start_line:
		s = line.split()
		s[5] = s[5].replace("\"", "")
		s[0] = s[0].replace("\"", "")
		ener.append(float(s[5]))
		ener_l.append(s[0])
	if nline <= (lz + start_line + 2) and nline > (lz + start_line):
		s = line.split()
		del s[0]
		del s[0]
		del s[len(s) - 1]
		ticks.append(s)
	if nline > (lz + start_line + 2):
		line = line.replace("\"", "")
		line = line.replace(",", "")
		y = ticks[1][yi]
		yi = yi - 1
		for i in range(len(line) - 1):
			zc = line[i]
			zi = ener_l.index(zc)
			z = ener[zi]
			x = ticks[0][i]		
			fw.write(str(x) + "\t" + str(y) + "\t" + str(z) + "\n")
		
	if line[0] == "\"" and nline < start_line:
		s = line.split()
		for i,a in enumerate(s):
			s[i] = a.replace("\"", "")
		lx = int(s[0])
		ly = int(s[1])
		lz = int(s[2])
		yi = ly
		start_line = nline

f.close()
fw.close()
		
