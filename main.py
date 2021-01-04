"""
function to generate 2D shape stimulus sets, heavily inspired by Higgins et al 2016

Each image consists of a geometric shape (polygon, ellipse, star) on a (default: black) background. 
Individual shape instances can be modulated parametrically in terms of
- translation (x,y)
- rotation
- scale 
- colour

Timo Flesch, 2017
"""
import cairo 
import argparse
import numpy as np
from paint_studio.painter import drawStimuli
from fio.saver            import saveData


# PARAMETERS ----------------------------------------------------------------------------
parser = argparse.ArgumentParser()
# general -------------------------------------------------------------------------------
parser.add_argument('--outdir','-o',           type=str,   nargs='+', default='./output/', 
	                                           help='Output directory (default: ./output/')
parser.add_argument('--name',                  type=str,   nargs='+', default=['stim2D_'],
                                               help='File Name (default: stim2D_')
parser.add_argument('--parallel',              type=int,   nargs=1,   default=0, 
	                                           help='Do Parallel Processing (default: 0)')

# canvas --------------------------------------------------------------------------------
parser.add_argument('--canvas_size',           type=int,   nargs='+', default=[250, 250],
                                               help='Size of Image Canvas (default: 250x250px)')
parser.add_argument('--canvas_bgcol',          type=float, nargs='+', default=[0.,0.,0.], 
	                                           help='Background Colour of Image Canvas (RGB,default: 0 0 0)')

# stimuli -------------------------------------------------------------------------------
parser.add_argument('--num_stimuli',           type=int,   nargs=1,   default=1, 
	                                           help='Number of stimuli per shape to generate (default: 1)') 
parser.add_argument('--num_transformations',   type=int,              default=0, 
	                                           help='Number of linearly spaced transformations (default:0)')
parser.add_argument('--shapes',                type=str,   nargs='+', default=['rect','ellipse', 'poly6', 'star5'], 
	                                           help='Shapes (rect, polyNUM,starNUM, ellipse) ')
parser.add_argument('--to_transform',          type=str,   nargs='+', default=[],
	                                           help='dimensions to transform with num_transformations. \
	                                           All other dims kept constant (scale,rota,trx,try,colour; default: None)')
parser.add_argument('--stim_poly_size',        type=int,                default=20,
	                                           help='Polygon "Radius"  (default: 50)')
parser.add_argument('--stim_star_size',        type=float,   nargs='+', default=[20,10],
	                                           help='Star Radii (outer, inner; default: [50,25])')
parser.add_argument('--stim_ellipse_ratio',    type=float, nargs='+', default=[1,.5],
	                                           help='Scaling of Circle to generate Ellipse')
parser.add_argument('--stim_rect_ratio',    type=float, nargs='+', default=[.5,1],
	                                           help='Scaling of square to generate rect')
parser.add_argument('--stim_scale',            type=float, nargs='+', default=[1,1],
	                                           help='Stimulus Scaling (default: (1,1)')
parser.add_argument('--stim_rota',             type=float,            default=0,
                                               help='Stimulus Rotation (deg; default: 0)')
parser.add_argument('--stim_trx',              type=float,             default=125,
	                                           help='Stimulus Translation along x (default: centre)')
parser.add_argument('--stim_try',              type=float,             default=125,
	                                           help='Stimulus Translation along y (default: 0)')
parser.add_argument('--stim_colour',           type=float,  nargs='+', default=[1., 1., 1.],
	                                           help='Stimulus Colour (default: [1.,1.,1.]')

# transformation ranges -----------------------------------------------------------------
parser.add_argument('--rng_ratio',             type=float, nargs='+', default=[.2, 5.],
                                               help='Shape width to height ratio (min,max; defaults:[.2, 5.]')
parser.add_argument('--rng_trx',               type=float, nargs='+', default=[.10, .90],
                                               help='Translation along x in decimal fractions (min,max; defaults:[.05, .95]')
parser.add_argument('--rng_try',               type=float, nargs='+', default=[.10, .90], 
	                                           help='Translation along y in decimal fractions (min,max; defaults:[.05, .95]')
parser.add_argument('--rng_rota',              type=int,   nargs='+', default=[-45, 45], 
	                                           help='Rotation in deg (min,max; defaults:[-45, 45]')
parser.add_argument('--rng_scale',             type=float, nargs='+', default=[.5, 1.5],
                                               help='Scale decimal fractions (min,max; defaults:[.2, 1.]')


FLAGS,_ = parser.parse_known_args() # ignore unspecified args
FLAGS.rng_trx = np.multiply(FLAGS.rng_trx,FLAGS.canvas_size)
FLAGS.rng_try = np.multiply(FLAGS.rng_try,FLAGS.canvas_size)
print(FLAGS)

def main(argv=None):	
	all_IMGs,all_idces = drawStimuli(FLAGS)
	data = {}
	data['images'] = all_IMGs # store all the images
	data['params'] = vars(FLAGS) # store all the parameters
	data['idces']  = all_idces  # for each image, store the feature values. (feature correspondence encoded in FLAGS.to_transform (same order))
	saveData(data,FLAGS.to_transform,FLAGS.shapes,FLAGS.outdir)
if __name__ == '__main__':
	""" start the fun"""
	main()
