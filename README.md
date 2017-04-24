# mapnik-scalebar
A quick and dirty PIL-based scale bar generator for Mapnik maps

This repository contains a single Python function called `addScaleBar`, which is designed to be a quick and easy (if slightly inelegant) way to add a 'quick and dirty' scale bar to a Mapnik map using PIL. It works out how long it wants to be based upon the size of the map, and draws itself to that size. Simple!

To use it, you simply you pass three arguments to the `addScaleBar` function:

* `m`: the `mapnik` `Map` object for which the scale bar needs to be drawn
* `mapImg`: `PIL` `Image` object for the (already rendered) mapnik map
* `left`:	`Boolean` value describing whether it should be drawn on the left (`True`) or right (`False`)

For example:

```python
from PIL import Image
from scalebar import addScaleBar

...

# render mapnik map to file
mapnik.render_to_file(m, 'output/map.png', 'png')

# open that file in PIL
mapImg = Image.open('output/map.png')

# add a scalebar to the map
addScaleBar(m, mapImg, True)

# save the image (with scalebar) to the map
mapImg.save('output/map2.png', "PNG")
```

This function does nothing fancy, you can't tell it how long you want the scalebar to be, what colour, what units, or where on the map to go (other than left or right). It is purely intended as a cheap and nasty approach, and one that you can pull to bits and edit in order to make your own scale bars...
