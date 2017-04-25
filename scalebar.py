"""
Draw a quick and dirty scale bar onto a mapnik map

@author jonnyhuck
"""

import mapnik
from math import floor, log10
from PIL import Image, ImageDraw, ImageFont

def addScaleBar(m, mapImg, left=False):
	"""
	* Add a scalebar to a map, at a sensible width of approx 20% the width of the map
	*
	* Parameters:
	*  - m: 		mapnik Map object
	*  - mapImg:	PIL Image object for the exported mapnik map
	*  - left:	boolean value describing whether it should be drawn on the left (True) or right (False)
	"""

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
	
	# get PIL context to draw on
	draw = ImageDraw.Draw(mapImg)
	
	# get the dimensions of the text
	tw, th = draw.textsize(scaleText)
	
	# prepare a font
	font = ImageFont.truetype('./open-sans/OpenSans-Regular.ttf', 12)

	# set scale bar positioning parameters
	barBuffer  = 5	# distance from scale bar to edge of image
	lBuffer    = 5	# distance from the line to the end of the background
	tickHeight = 12	# height of the tick marks
	
	# draw scale bar on bottom left...
	if left:
	
		# add background
		draw.rectangle([(pxScaleBar+lBuffer+lBuffer+barBuffer, 
			m.height-barBuffer-lBuffer-lBuffer-tickHeight),
			(barBuffer,m.height-barBuffer)], 
			outline=(0,0,0), fill=(255,255,255))
	
		# add lines
		draw.line([
			(lBuffer+pxScaleBar+barBuffer, m.height-tickHeight-barBuffer), 
			(lBuffer+pxScaleBar+barBuffer, m.height-lBuffer-barBuffer), 
			(lBuffer+barBuffer, m.height-lBuffer-barBuffer), 
			(lBuffer+barBuffer, m.height-tickHeight-barBuffer)], 
			fill=(0, 0, 0), width=1)
	
		# add label
		draw.text(( ((lBuffer+pxScaleBar+barBuffer+lBuffer)/2)-tw/2, 
			m.height-barBuffer-lBuffer-lBuffer-th), 
			scaleText, fill=(0,0,0), font=font)
	
	# ...or bottom right
	else:
			
		# add background
		draw.rectangle([(m.width-pxScaleBar-lBuffer-lBuffer-barBuffer, 
			m.height-barBuffer-lBuffer-lBuffer-tickHeight),
			(m.width-barBuffer,m.height-barBuffer)], 
			outline=(0,0,0), fill=(255,255,255))
	
		# add lines
		draw.line([
			(m.width-lBuffer-pxScaleBar-barBuffer, m.height-tickHeight-barBuffer), 
			(m.width-lBuffer-pxScaleBar-barBuffer, m.height-lBuffer-barBuffer), 
			(m.width-lBuffer-barBuffer, m.height-lBuffer-barBuffer), 
			(m.width-lBuffer-barBuffer, m.height-tickHeight-barBuffer)], 
			fill=(0, 0, 0), width=1)
	
		# add label
		draw.text(( 
			(m.width-lBuffer-lBuffer-pxScaleBar/2) - tw/2, 
			m.height-barBuffer-lBuffer-lBuffer-th), 
			scaleText, fill=(0,0,0), font=font)