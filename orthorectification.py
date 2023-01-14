import matplotlib.colors as colors
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
# from termcolor import colored
from zipfile import ZipFile
from os.path import join
from glob import iglob
import pandas as pd
import numpy as np
import subprocess
import snappy
import jpy
pd.options.display.max_colwidth=80
def output_view(product,band, min_value_VV, max_value_VV, min_value_VH, max_value_VH):
   band_data_list=[]
   for i in band:
       band=product.getBand(i)
       w=band.getRasterWidth()
       h=band.getRasterHeight()
       band_data=np.zeros(w*h, np.float32)
       band.readPixels(0, 0, w, h, band_data)
       band_data.shape=h,w
       band_data_list.append(band_data)
   fig, (ax1,ax2)=plt.subplots(1,2,figsize=(16.16))
   ax1.imshow(band_data_list[0],cmap='gray',vmin= min_value_VV, vmax=max_value_VV)
   ax1.set_title(output_bands[0])
   ax2.imshow(band_data_list[1],cmap='gray',vmin= min_value_VH, vmax=max_value_VH)
   ax2.set_title(output_bands[1])
   for ax in fig.get_axes:
       ax.label_outer()
product_path="C:\\Users\\mrmzm\\anaconda3\\envs\\snap\\"
input_S1_files= sorted(list(iglob(join(product_path,"**",'*S1*.zip'))))
name, sensing_mode, product_type, polarization, height, width, band_names= ([] for i in range(7))

for i in input_S1_files:
   sensing_mode.append(i.split("_")[3])
   product_type.append(i.split("_")[4])
   polarization.append(i.split("_")[-6])
   s1_read=snappy.ProductI0.readProduct(i)
   print(type(s1.read))
   name.append(s1_read.getName())
   height.append(s1_read.getSceneRasterHeight())
   width.append(s1_read.getSceneRasterWidth())
   band_names.append(s1_read.getBandNames())
 
df_s1_read=pd.DataFrame({'Name': name, 'Sensing Mode': sensing_mode, 'Product Type':product_type,'Polarization':polarization,'Height':height})

x, y, width, height=12000, 8000, 5500,5500
# Subset Operator snappy
 
parameters=snappy.HashMap()
parameters.put('copyMetadata', True)
parameters.put('region',"%s,%s,%s,%s" % (x, y, width, height))
subset=snappy.GPF.createProduct('Subset', parameters, s1_read)
list(subset.getBandNames())
 
output_bands=['Amplitude_VV' ,'Amplitude_VH']
output_view(subset, output_bands,41, 286, 28, 166)
