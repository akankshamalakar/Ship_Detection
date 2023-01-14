import snappy
from snappy import ProductIO, GPF, ProgressMonitor

HashMap = snappy.jpy.get_type('java.util.HashMap')
product = ProductIO.readProduct('subTEST.dim')

### MAKING SHAPE
shapeFile = 'geometry_Polygon.shp'
params3 = HashMap()
params3.put('vectorFile', shapeFile)
params3.put('separateShapes', False)  # ?
target0 = GPF.createProduct('Import-Vector', params3, product)

ProductIO.writeProduct(target0, "TEST_POLYGON", 'BEAM-DIMAP')  # This product has the shape added.


### MAKING IMAGE
JPY = snappy.jpy
imageIO = JPY.get_type('javax.imageio.ImageIO')
File = JPY.get_type('java.io.File')

band = target0.getBand('Amplitude_VV')
image = band.createColorIndexedImage(ProgressMonitor.NULL)
name = File('test.png')
imageIO.write(image, 'PNG', name)  # But the shape is not added to the image.