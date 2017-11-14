"""
geometric transformations (translation,rotation,scale)
colour transformations (gradients)

Timo Flesch, 2017
"""
import cairo
import  math

def translateShape(ctx,dx=0,dy=0):
	ctx.translate(dx,dy)
	return ctx

def rotateShape(ctx,angle):
	ctx.rotate(math.radians(angle))
	return ctx
	
def scaleShape(ctx,scale):
	ctx.scale(scale[0],scale[1])
	return ctx

def colouriseShape(ctx,newCol):
	ctx.set_source_rgb(newCol[0],newCol[1],newCol[2])
	return ctx


