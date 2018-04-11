"""
Create a simple map using Mapnik to demonstrate the scalebar usage.
"""
import mapnik
import scalebar
from PIL import Image

# make a map to draw to
m = mapnik.Map(800,400)
m.background = mapnik.Color('white')

# style the map
style = mapnik.Style()
rule = mapnik.Rule()
rule.symbols.append(mapnik.PolygonSymbolizer(mapnik.Color('#c0d9a2')))
rule.symbols.append(mapnik.LineSymbolizer(mapnik.Color('black'), 0.5))
style.rules.append(rule)
m.append_style('Countries_Style',style)

# add the layer
layer = mapnik.Layer('Countries_Layer')
# layer.datasource = mapnik.Shapefile(file='data/110m-admin-0-countries/ne_110m_admin_0_countries.shp')
layer.datasource = mapnik.Shapefile(file='data/gb/ne_110m_admin_0_countries.shp')
layer.styles.append('Countries_Style')
m.layers.append(layer)

'''
* Print whole world
'''
 
# # render the map to an image file
# m.zoom_all()
# mapnik.render_to_file(m,'images/world.png', 'png')
# im = Image.open('images/world.png')
# 
# # add scalebar
# sb = scalebar.getScaleBar(m)
# im.paste(sb, (5, 5))
#
# # save output
# im.save('images/world.png', "png")

'''
* Print UK using wgs84 and OSGB
'''
 
# render the map to an image file
m.zoom_all()
mapnik.render_to_file(m,'images/wgs84.png', 'png')
im = Image.open('images/wgs84.png')

# add scalebar
sb = scalebar.getScaleBar(m)
im.paste(sb, (5, 5))

# save output
im.save('images/wgs84.png', "png")

# project map
m.srs = '+proj=tmerc +lat_0=49 +lon_0=-2 +k=0.9996012717 +x_0=400000 +y_0=-100000 +ellps=airy +datum=OSGB36 +units=m +no_defs'

# zoom the map so that it shows all of the data
m.zoom_all()

# render the map to an image file
mapnik.render_to_file(m,'images/osgb.png', 'png')
im = Image.open('images/osgb.png')

# add scalebar
sb = scalebar.getScaleBar(m)
im.paste(sb, (5, 5))

# save output
im.save('images/osgb.png', "png")


mapnik.save_map(m, 'out.xml')


# for l in m.layers:
# 	for n in l.styles:
# 		for r in  m.find_style(n).rules:
# 			print dir(r)

# show the final image
# im.show()