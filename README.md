# mapnik-scalebar
A quick and dirty PIL-based scale bar generator for Mapnik maps

## Dependencies

* [Mapnik](http://mapnik.org/) Python bindings
* PIL / [Pillow](https://python-pillow.org/)

## Usage

This repository contains a single Python function called `addScaleBar`, which is designed to be a quick and easy (if slightly inelegant) way to add a 'quick and dirty' scale bar to a Mapnik map using PIL. It works out how long it wants to be based upon the size of the map, and draws itself to that size. Simple!

To use it, you simply you pass three arguments to the `addScaleBar` function:

* `m`: the `mapnik` `Map` object for which the scale bar needs to be drawn
* `mapImg`: `PIL` `Image` object for the (already rendered) mapnik map
* `left`:	`Boolean` value describing whether it should be drawn on the bottom left (`True`) or bottom right (`False`) of the map

For example:

```python
from PIL import Image
from scalebar import addScaleBar

# make a mapnik map
m = mapnik.Map(600, 600)

...

# render mapnik map to file
mapnik.render_to_file(m, 'map.png', 'png')

# open that file in PIL
mapImg = Image.open('map.png')

# add a scalebar to the bottom left of the map
addScaleBar(m, mapImg, True)

# save the image (with scalebar) to the map
mapImg.save('map.png', "PNG")
```

This function does nothing fancy, you can't tell it how long you want the scalebar to be, what colour, what units, or where on the map to go (other than bottom-left or bottom-right). It is purely intended as a cheap and nasty approach, and one that you can pull to bits and edit in order to make your own scale bars...

## The Open-Sans Font
For convenience, the [Open-Sans](https://fonts.google.com/specimen/Open+Sans) font has been bundled with this software. This is available under the [Apache 2.0](http://www.apache.org/licenses/LICENSE-2.0) license. This copy was obtained from [Google Fonts](https://fonts.google.com/specimen/Open+Sans).