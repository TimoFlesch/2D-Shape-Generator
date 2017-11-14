"""
various tools to work with a cairo canvas
Timo Flesch, 2017
"""

import cairo
import numpy as np
# from colour import Color


def makeSurface(ssize):
	img = cairo.ImageSurface(cairo.FORMAT_ARGB32,ssize[0],ssize[1])	
	return img

def makeContext(img):
	return cairo.Context(img)

def makeCanvas(imsize,bgcol):
	img = makeSurface(imsize)
	ctx = makeContext(img)
	ctx.set_source_rgb(bgcol[0],bgcol[1],bgcol[2])
	ctx.paint()
	return img,ctx


def clearContext(ctx,col):
	ctx.set_source_rgb(col[0],col[1],col[2])
	ctx.paint()
	return ctx


# def colourGradient(col1,col2,numCols=10):
# 	#TODO define colourmaps
# 	c1 = Color(col1)
# 	c2 = Color(col2)
# 	colors = list(c1.range_to(c2,numCols))
# 	colors_RGB = [c.rgb for c in colors]
# 	return colors_RGB

def colourGradient(numCols=10):
	cols = [(1-ii,0,ii) for ii in np.linspace(0,1,numCols)]
	return cols 

def makeValueDict(FLAGS):
	# generate arrays of linearily spaced parameter values for each dimension to manipulate
	valDict = {}
	for ii,dim in enumerate(FLAGS.to_transform):				
		if dim=='colour':
			valDict[dim] = colourGradient(FLAGS.num_transformations)
		elif dim=='scale':
			valDict[dim] = [(jj,jj) for jj in np.linspace(getattr(FLAGS,'rng_'+dim)[0],getattr(FLAGS,'rng_'+dim)[1],num=FLAGS.num_transformations)]
		else:
			valDict[dim] = np.linspace(getattr(FLAGS,'rng_'+dim)[0],getattr(FLAGS,'rng_'+dim)[1],num=FLAGS.num_transformations)
			
	return valDict
	