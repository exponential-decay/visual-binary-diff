# -*- coding: utf-8 -*-

import os
import sys
import math
import argparse
import StringIO

from PIL import Image
from PIL import PngImagePlugin

purple = "#551A8B"
yellow = "#fff44f"

def fadetuple(color):
	x = 2
	return (color[0]-x, color[1]-x, color[2]-x)

def write_to_file(output):
   f = open("diff" + ".png", "wb")
   f.write(output.getvalue())
   f.close()

def HEXtoRGB(colorstring):
   #courtesy of code recipes. getrgb from PIL would be better (if it worked)
   colorstring = colorstring.strip()
   if colorstring[0] == '#': 
		colorstring = colorstring[1:]
   r, g, b = colorstring[:2], colorstring[2:4], colorstring[4:]
   r, g, b = [int(n, 16) for n in (r, g, b)]
   return (r, g, b)

def drawpng(comparelist):

	l1 = comparelist

	#l1 = [0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1]
	#l1 = [0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1]

	bytes = 100
	pixsize = 25

	#Optional... Bytes, or sqrt... try to be dynamic...
	bytes = min(int(math.sqrt(len(l1))+1), bytes)

	#Bytes then used to configure the rest...
	canvas_x = pixsize * bytes
	canvas_y = (int(len(l1) / bytes)+1) * pixsize

	if canvas_x > canvas_y:
		canvas_y = canvas_x + (pixsize * 2)

	image = Image.new("RGB", (canvas_x, canvas_y), color=HEXtoRGB("#000000"))
	color = HEXtoRGB(purple)

	xpos = 0
	ypos = 0

	xloc = 0
	yloc = 0

	#for each entry, create a new set of pixels, e.g. 10x10
	for i, x in enumerate(l1):
		if x == 0:
			color = HEXtoRGB(purple)
		if x == 1: 
			color = HEXtoRGB(yellow)

		ypos = yloc
		for y1 in range(pixsize):
			for x1 in range(pixsize):
				image.putpixel((xpos+x1, ypos), color)
			ypos = ypos + 1
			color = fadetuple(color)

		xpos = xpos + pixsize
	
		if (i+1)%bytes == 0:
			yloc = yloc + pixsize
			xpos = 0

	output = StringIO.StringIO()
	image.save(output, "PNG")
	write_to_file(output)
	return

#only consider files of equal size...
def comparesize(f1, f2):
	if os.stat(f1).st_size != os.stat(f2).st_size:
		return False
	return True

def imagefiles(f1, f2):
	comparelist = []
	if comparesize(f1, f2):
		with open(f1) as a:
			with open(f2) as b:
				for line in a:
					for byte in line:
						if byte != b.read(1):
							comparelist.append(1)
						else:
							comparelist.append(0)
		drawpng(comparelist)
	else:
		sys.stderr.write("Filesizes do not match.")
		sys.exit(1)
	return

def main():

	#	Handle command line arguments for the script
	parser = argparse.ArgumentParser(description='Draw an image showing the difference between two files.')
	parser.add_argument('--f1', help='Mandatory: File 1.', default=False)
	parser.add_argument('--f2', help='Mandatory: File 2.', default=False)

	if len(sys.argv) < 2:
		parser.print_help()
		sys.exit(1)

	#	Parse arguments into namespace object to reference later in the script
	global args
	args = parser.parse_args()

	if args.f1 and args.f2:
		imagefiles(args.f1, args.f2)
	else:
		parser.print_help()
		sys.exit(1)

if __name__ == "__main__":      
   main()
