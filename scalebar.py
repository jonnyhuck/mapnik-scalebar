"""
Draw a quick and dirty scale bar onto a mapnik map

@author jonnyhuck
"""

import mapnik
from pyproj import Proj
from math import floor, log10, ceil, radians, cos, hypot
from PIL import Image, ImageDraw, ImageFont

def equirectangularApproxDistance(x1, y1, x2, y2, R=6371008.771415):
	"""
	Equirectangular approximation distance measurement used to find the length of a degree in an equirectangular 
	projection - this reflects how the map will be projected if no map is given
	"""
	y1 = radians(y1)
	x1 = radians(x1)
	y2 = radians(y2)
	x2 = radians(x2)
	x = (x2-x1) * cos((y1+y2) / 2)
	y = (y2-y1)
	return hypot(x, y) * R


def mm2px(mm, dpi=90.7):
	"""
	1 inch = 25.4mm 96dpi is therefore...
	"""
	return int(ceil(mm * dpi / 25.4))


def getScaleBar(m, R=6371008.771415, dpi=90.7):
	"""
	* Construct a quick and dirty scalebar, at a sensible width of approx 20% the width of the map
	* Returned as a PIL Image object
	*
	* Map should be projected. If not, scale will be estimated based upon equirectangular projection
	*
	* Parameters:
	*  - m: 	Mapnik Map object 
	*  - R: 	Earth Radius (for equirectangular approximation) - default WGS84
	*  - dpi:	The dpi (resolution at which the map will be printed) - default OGC definition (0.28mm per px)
	"""

	# is this a projected map? If not, convert scale to m
	if Proj(m.srs).is_latlong():
	
		# get the extent of the map
		centre = m.envelope().center()
		
		# get the m per pixel on the map (multiply value by length of a degree in m)
		mPerPx = m.scale() * equirectangularApproxDistance(centre.x, centre.y, centre.x+1, centre.y, R)
		
		print
		print "Warning: Your map is not projected, scale estimated using equrectangular approximation"
		
	else:
	
		# get the m per pixel on the map
		mPerPx = m.scale()

	# how many metres is 20% of the width of the map?
	twentyPc = m.width * 0.2 * mPerPx

	# get the order of magnitude
	oom = 10 ** floor(log10(twentyPc))

	# get the desired width of the scalebar in m
	mScaleBar = round(twentyPc / oom) * oom

	# get the desired width of the scalebar in px
	pxScaleBar = round(mScaleBar/mPerPx)

	# make some text for the scalebar (sort units)
	if oom >= 1000:
		scaleText = str(int(mScaleBar/1000)) + "km"
	else:
		scaleText = str(int(mScaleBar)) + "m"
		
	# set scale bar positioning parameters
	lBuffer    = mm2px(2)	# distance from the line to the end of the box
	tickHeight = mm2px(3)	# height of the tick marks
	
	# new image for scalebar
	scalebarImg = Image.new('RGB', (int(pxScaleBar+lBuffer+lBuffer), lBuffer+lBuffer+tickHeight), 'white')
	
	# get PIL context to draw on
	sb_draw = ImageDraw.Draw(scalebarImg)

	# prepare a font
	font = ImageFont.truetype('./open-sans/OpenSans-Regular.ttf', 12)
	
	# get the dimensions of the text
	tw, th = sb_draw.textsize(scaleText, font=font)
	
	sbw, sbh = scalebarImg.size
		
	# add background
	sb_draw.rectangle([
		(1, 1), (sbw-1, sbh-1)], 
		outline=('black'), fill=('white'))

	# add lines
	sb_draw.line([
		(lBuffer, sbh-tickHeight-lBuffer), 
		(lBuffer, sbh-lBuffer),
		(lBuffer+pxScaleBar, sbh-lBuffer), 
		(lBuffer+pxScaleBar, sbh-tickHeight-lBuffer)], 
		fill='black', width=1)
 
	# add label
	sb_draw.text(
		((sbw-tw)/2, sbh-tickHeight-lBuffer-mm2px(1.5)), 
		scaleText, fill='black', font=font)
	
	return scalebarImg