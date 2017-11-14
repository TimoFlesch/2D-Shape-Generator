import cairo
import itertools
import numpy as np

import matplotlib.pyplot as plt
# custom:
from paint_studio.equipment       import *
from paint_studio.shapes          import *
from paint_studio.transformations import *


def drawStimuli(FLAGS):
	"""
	draws stimuli for all requested combinations of parameters
	and returns a dictionary with numpy arrays
	"""
	img,ctx = makeCanvas(FLAGS.canvas_size,FLAGS.canvas_bgcol)
	img_centre = np.floor(img.get_width()/2), np.floor(img.get_height()/2)
	# make array with all combinations of feature levels 
	all_idces = list(itertools.product(range(FLAGS.num_transformations),repeat=len(FLAGS.to_transform)))
	# make loop-up dictionary with feature values within requested range for each feature dimension
	all_IMGs = np.zeros((len(FLAGS.shapes),len(all_idces),FLAGS.canvas_size[0],FLAGS.canvas_size[1],3),np.uint8)
	valueDict = makeValueDict(FLAGS)
	# iterate through shapes and exemplars, generate one image per iteration (TODO: parallelise with second for loop)
	for ii,stimulus_shape in enumerate(FLAGS.shapes):							
		for jj,idx_tuple in enumerate(all_idces):				
			ctx.save()
			ctx,img_mat,img = makeStimulus(img,FLAGS,idx_tuple,valueDict,img_centre,stimulus_shape,ctx,jj)	
			# store in numpy array ii,jj, blah blah
			all_IMGs[ii,jj,:,:,:] = img_mat

			ctx.restore()
			ctx = clearContext(ctx,FLAGS.canvas_bgcol)	
	return all_IMGs,all_idces



def makeStimulus(img,FLAGS,idces,valueDict,centre,stim_shape,ctx,imgID):
	"""
	draws a stimulus with selected feature values
	"""

	# this loop overwrites the defaults for each feature dimension that is parametrically varied (e.g. scale, rota)
	# by values corresponding to the indexed positions in their range vectors
	print('-----new stimulus-------')	
	for ii,dim in enumerate(FLAGS.to_transform): # iterate through dimensions to transform
		# for selected dimension (e.g. scale), retrieve vector of requested feature values from dictionary
		vals = valueDict[dim]		
		# set the "default" for this particular feature 
		setattr(FLAGS,'stim_'+dim,vals[idces[ii]])
		print(stim_shape + ' ' + dim + str(getattr(FLAGS,'stim_'+dim)))
	# now, draw a shape with the new set of parameters
	ctx = drawShape(ctx,FLAGS,
			[0,0],
			stim_shape)
	tmp = np.frombuffer(img.get_data(),np.uint8)
	tmp.shape = [FLAGS.canvas_size[0],FLAGS.canvas_size[1],4]
	tmp = tmp[:,:,0:3]
	img.write_to_png('img_' + stim_shape + str(imgID) + '.png')
	return ctx,tmp,img 


def drawShape(ctx,FLAGS,centre,stimShape):	
	ctx = translateShape(ctx,centre[0],centre[1])
	ctx = translateShape(ctx,FLAGS.stim_trx,FLAGS.stim_try)
	ctx = rotateShape(ctx,FLAGS.stim_rota)			
	ctx = scaleShape(ctx,FLAGS.stim_scale)	
	ctx = colouriseShape(ctx,FLAGS.stim_colour)
	if stimShape=='rect':				
		ctx = drawRect(ctx,centre,FLAGS.stim_poly_size,FLAGS.stim_rect_ratio)		
	elif stimShape[0:4]=='poly':
		ctx = drawPolygon(ctx,centre,FLAGS.stim_poly_size,numVertices=int(stimShape[4:]))
	elif stimShape[0:4]=='star':
		ctx = drawStar(ctx,centre,FLAGS.stim_star_size[0],FLAGS.stim_star_size[1],numVertices=int(stimShape[4:]))	
	elif stimShape=='circle':
		ctx = drawCircle(ctx,centre,FLAGS.stim_poly_size)
	elif stimShape=='ellipse':
		ctx = drawEllipse(ctx,centre,FLAGS.stim_poly_size,FLAGS.stim_ellipse_ratio)

	ctx.fill()
	return ctx
