import numpy as np
import pyvo as vo
import matplotlib
import matplotlib.pyplot as plt
from pasta.augment import inline

from astropy.io import fits
import astropy.coordinates as coord


import warnings

warnings.filterwarnings("ignore", module="astropy.io.votable.*")
warnings.filterwarnings("ignore", module="pyvo.utils.xml.*")


class Images:

    def __init__(self, serviceType, waveBand, keyword, coord, size):
        self.serviceType = serviceType
        self.waveBand = waveBand
        self.keyword = keyword
        self.coord = coord
        self.size = size

    def getUltravioletUrl(self):
        uv_services = vo.regsearch(servicetype = self.serviceType, waveband = self.waveBand)
        uvot_services = vo.regsearch(servicetype=self.serviceType, waveband=self.waveBand, keywords=[self.keyword])

        coords = coord.SkyCoord.from_name(self.coord)

        im_table = uvot_services[0].search(pos=coords, size=self.size, format='image/jpeg')
        im_table.to_table()

        url = im_table[0].getdataurl()
        return(url)

    def getUltravioletFits(self):
        uv_services = vo.regsearch(servicetype=self.serviceType, waveband=self.waveBand)
        uvot_services = vo.regsearch(servicetype=self.serviceType, waveband=self.waveBand, keywords=[self.keyword])

        coords = coord.SkyCoord.from_name(self.coord)

        im_table = uvot_services[0].search(pos=coords, size= self.size, format='image/fits')

        fitUrl = im_table[0].getdataurl()
        #print(fitUrl)
        return(fitUrl)

#test = Images("image", "uv", "swift", "m51", 0.2)
#x = test.getUltravioletUrl()
#print(x)
#test.getUltravioletFits()