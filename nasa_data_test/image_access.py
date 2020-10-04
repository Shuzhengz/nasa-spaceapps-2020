import numpy as np

import matplotlib
import matplotlib.pyplot as plt
from pasta.augment import inline

import pyvo as vo

from astropy.io import fits
import astropy.coordinates as coord
# For downloading files
from astropy.utils.data import download_file

import aplpy
from IPython.display import Image as ipImage, display

# There are a number of relatively unimportant warnings that show up, so for now, suppress them:
import warnings
warnings.filterwarnings("ignore", module="astropy.io.votable.*")
warnings.filterwarnings("ignore", module="pyvo.utils.xml.*")

uv_services = vo.regsearch(servicetype='image',waveband='uv')
uv_services.to_table()['ivoid','short_name','res_title']

uvot_services = vo.regsearch(servicetype='image',waveband='uv',keywords=['swift'])
uvot_services.to_table()['ivoid','short_name','res_title']

coords = coord.SkyCoord.from_name("m51")

im_table = uvot_services[0].search(pos=coords,size=0.2,format='image/jpeg')
im_table.to_table()

url = im_table[0].getdataurl()
print(url)

img = ipImage(url=im_table[0].getdataurl())
display(img)

#  Do the search again asking for FITS
im_table = uvot_services[0].search(pos=coords,size=0.2,format='image/fits')

#  Hand the url of the first result to fits.open()
hdu_list = fits.open(im_table[0].getdataurl())
hdu_list.info()

plt.imshow(hdu_list[0].data, cmap='gray', origin='lower',vmax=0.1)

gc = aplpy.FITSFigure(hdu_list,figsize=(5, 5))
gc.show_grayscale(stretch='log', vmax=0.1)

services = vo.regsearch(servicetype='image', keywords=['sloan'], waveband='optical')
services.to_table()[np.where(np.isin(services.to_table()['short_name'], b'SDSSDR7'))]['ivoid', 'short_name']

heasarc_dr7_service = [s for s in services if 'SDSSDR7' in s.short_name and 'heasarc' in s.ivoid][0]

sdss_table_heasarc = heasarc_dr7_service.search(pos=coords,size=0.2,format='image/fits')
sdss_table_heasarc.to_table()

## If you only run this once, you can do it in memory in one line:
##  This fetches the FITS as an astropy.io.fits object in memory
# hdu_list = sdss_table_heasarc[0].getdataobj()
## But if you might run this notebook repeatedly with limited bandwidth,
##  download it once and cache it.

#  Get the filter g version
file_name=download_file(sdss_table_heasarc[0].getdataurl(),cache=True)
hdu_list = fits.open(file_name)

plt.imshow(hdu_list[0].data, cmap='gray', origin='lower', vmax=1200,vmin=1010)

jhu_dr7_service = [s for s in services if 'SDSSDR7' in s.short_name and 'jhu' in s.ivoid][0]

# Note: jhu_dr7_service access url has hard-wired "format=image/fits".
# If you specify anythign else, it errors. If you specify nothing,
# then the search() method puts "format=all", which errors. So specify empty string for now.
sdss_table_jhu=jhu_dr7_service.search(pos=coords,size=0.2, format='')
sdss_table_jhu.to_table().show_in_notebook(display_length = 5)

#  Get the filter g version
file_name=download_file(sdss_table_jhu[1].getdataurl(),cache=True)
hdu_list = fits.open(file_name)
plt.imshow(hdu_list[0].data, cmap='gray', origin='lower',vmax=1200,vmin=1010)