# suppress some specific warnings that are not important
import warnings
warnings.filterwarnings("ignore", module="astropy.io.votable.*")
warnings.filterwarnings("ignore", module="pyvo.utils.xml.*")

import io
import numpy as np

# Astropy imports
import astropy.units as u
import astropy.constants as const
from astropy.coordinates import SkyCoord
from astropy.cosmology import Planck15
from astropy.io import votable as apvot

## Generic VO access routines
import pyvo as vo

coord = SkyCoord.from_name("m51")
print(coord)

services = vo.regsearch(servicetype='scs', keywords=['zcat'])
services.to_table()['ivoid', 'short_name', 'res_title']

## Use the one that's CFAZ.
##  Use list comprehension to check each service's short_name attribute and use the first.
cfaz_cone_service = [s for s in services if 'CFAZ' in s.short_name][0]

## We are searching for sources within 10 arcminutes of M51.
results = cfaz_cone_service.search(pos=coord, radius=10*u.arcmin)
results.to_table()

heasarc_tap_services = vo.regsearch(servicetype='tap', keywords=['heasarc'])
heasarc_tap_services.to_table()['ivoid', 'short_name', 'res_title']

heasarc_tables = heasarc_tap_services[0].service.tables
for tablename in heasarc_tables.keys():
    if "zcat" in tablename:
        heasarc_tables[tablename].describe()
        print("Columns={}".format(sorted([k.name for k in heasarc_tables[tablename].columns ])))
        print("----")



##  Inside the format call, the {} are replaced by the given variables in order.
##  So this asks for
##  rows of public.zcat where that row's ra and dec (cat.ra and cat.dec from the catalog)
##  are within radius 1deg of the given RA and DEC we got above for M51
##  (coord.ra.deg and coord.dec.deg from our variables defined above), and where
##  the bmag column is less than 14.
query = """SELECT ra, dec, Radial_Velocity, radial_velocity_error, bmag, morph_type FROM public.zcat as cat where 
    contains(point('ICRS',cat.ra,cat.dec),circle('ICRS',{},{},1.0))=1 and
    cat.bmag < 14
    order by cat.radial_velocity_error 
    """.format(coord.ra.deg, coord.dec.deg)

results = heasarc_tap_services[0].service.run_async(query)
#results=heasarc_tap_services[0].search(query)
results.to_table()

query = """SELECT ra, dec, Radial_Velocity, radial_velocity_error, bmag, morph_type FROM public.zcat as cat where 
    cat.bmag < 14 and cat.morph_type between 1 and 9 and cat.Radial_Velocity < 3000 
    order by cat.Radial_velocity 
    """.format(coord.ra.deg, coord.dec.deg)

results = heasarc_tap_services[0].service.run_async(query)
#results = heasarc_tap_services[0].search(query)
results.to_table()



query="""
    SELECT cat.ra, cat.dec, Radial_Velocity, bmag, morph_type
    FROM zcat cat, tap_upload.mysources mt 
    WHERE
    contains(point('ICRS',cat.ra,cat.dec),circle('ICRS',mt.ra,mt.dec,0.01))=1
    and Radial_Velocity > 0
    ORDER by cat.ra"""
zcattable = heasarc_tap_services[0].service.run_async(query, uploads={'mysources': 'data/my_sources.xml'})
#zcattable = heasarc_tap_services[0].search(query, uploads={'mysources': 'data/my_sources.xml'})
mytable = zcattable.to_table()
mytable

## The column 'radial_velocity' is c*z but doesn't include the unit; it is km/s
## Get the speed of light from astropy.constants and express in km/s
c = const.c.to(u.km/u.s).value
redshifts = mytable['radial_velocity']/c
mytable['redshift'] = redshifts
physdist = 0.05*u.Mpc # 50 kpc physical distance

angDdist = Planck15.angular_diameter_distance(mytable['redshift'])
angDrad = np.arctan(physdist/angDdist)
mytable['angDdeg'] = angDrad.to(u.deg)
mytable

## In memory only, use an IO stream.
vot_obj=io.BytesIO()
apvot.writeto(apvot.from_table(mytable),vot_obj)
## (Reset the "file-like" object to the beginning.)
vot_obj.seek(0)

query="""SELECT mt.ra, mt.dec, cat.ra, cat.dec, cat.Radial_Velocity, cat.morph_type, cat.bmag 
    FROM zcat cat, tap_upload.mytable mt 
    WHERE
    contains(point('ICRS',cat.ra,cat.dec),circle('ICRS',mt.ra,mt.dec,mt.angDdeg))=1
    and cat.Radial_Velocity > 0 and cat.radial_velocity != mt.radial_velocity
    ORDER by cat.ra"""
#  Currently broken due to a bug.
#mytable2 = heasarc_tap_services[0].service.run_async(query, uploads={'mytable':vot_obj})
mytable2 = heasarc_tap_services[0].search(query, uploads={'mytable':vot_obj})
vot_obj.close()
mytable2.to_table()