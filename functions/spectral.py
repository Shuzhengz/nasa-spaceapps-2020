import numpy as np
import matplotlib
import matplotlib.pyplot as plt

from astropy.table import Table
import astropy.io.fits as fits
from astropy.coordinates import SkyCoord

import pyvo as vo

import warnings

warnings.filterwarnings("ignore", module="astropy.io.votable.*")
warnings.filterwarnings("ignore", module="pyvo.utils.xml.*")


class Spectral:

    def __init__(self, serviceType, waveBand, name, coord, size):
        self.serviceType = serviceType
        self.waveBand = waveBand
        self.name = name
        self.coord = coord
        self.size = size

    def getSpectral(self):
        services = vo.regsearch(servicetype=self.serviceType, waveband=self.waveBand)
        services.to_table()['ivoid', 'short_name']

        chandra_service = [s for s in services if 'Chandra' in s.short_name][0]
        chandra_service.access_url

        Pos = SkyCoord.from_name(self.name)

        spec_tables = chandra_service.search(pos=Pos, diameter=0.1)
        spec_tables.to_table().show_in_notebook()

        Url = spec_tables[0].getdataurl()

        return(Url)

#test = Spectral("ssa", "x-ray", "Delta Ori", "m51", 0.2)
#test.getSpectral()