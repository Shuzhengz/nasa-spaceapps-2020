import io

import base64


from flask import Flask, Response, render_template, request

import urllib.request
import xmltodict
import ftplib

import numpy as np

import matplotlib
import matplotlib.pyplot as plt

from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure


from astropy.utils.data import download_file, get_pkg_data_filename
from astropy.io import fits

from astropy.visualization import astropy_mpl_style

plt.style.use(astropy_mpl_style)

app = Flask(__name__)

@app.route('/')
def view():
	all_xml_dict = []

	with ftplib.FTP('data.asc-csa.gc.ca') as ftp:
		try:
			ftp.login()
			ftp.cwd('/users/OpenData_DonneesOuvertes/pub/NEOSSAT/XML/')
			files = []

			filenames = ftp.nlst()

			iterations = 0

			for filename in filenames[::-1]:
				if iterations < 1:
					iterations += 1
					url = 'ftp://data.asc-csa.gc.ca/users/OpenData_DonneesOuvertes/pub/NEOSSAT/XML/' + filename
					response = urllib.request.urlopen(url).read()
					data = xmltodict.parse(response, dict_constructor=dict)
					all_xml_dict.append(data)
				if iterations == 1:
					break

		except ftplib.all_errors as e:
			print('FTP error:', e)

	'''get_image("")'''
	'''print(all_xml_dict[0]['FITSImage']['Image']['ImageFile'])'''

	'''# Generate plot
	fig = Figure()
	axis = fig.add_subplot(1, 1, 1)
	axis.set_title("title")
	axis.set_xlabel("x-axis")
	axis.set_ylabel("y-axis")
	axis.grid()
	axis.plot(range(5), range(5), "ro-")

	# Convert plot to PNG image
	pngImage = io.BytesIO()
	FigureCanvas(fig).print_png(pngImage)

	# Encode PNG image to base64 string
	pngImageB64String = "data:image/png;base64,"
	pngImageB64String += base64.b64encode(pngImage.getvalue()).decode('utf8')'''

	'''image_file = download_file('ftp://ftp.asc-csa.gc.ca/users/OpenData_DonneesOuvertes/pub/NEOSSAT/ASTRO/2018/284/TOI129/FINE_POINT/NEOS_SCI_2018284225800.fits')
	image_data = fits.getdata(image_file, ext=0)
	image_plt = plt.imshow(image_data, cmap='gray')'''

	'''get_image('ftp://ftp.asc-csa.gc.ca/users/OpenData_DonneesOuvertes/pub/NEOSSAT/NESS/2015/347-NESS/NEOS_SCI_2015347071100.fits')'''

	return render_template("viewer.html", message="message", test_obj=all_xml_dict)

@app.route('/detail')
def details():
	datetime = request.args.get('datetime', default = "-1", type = str)
	
	return render_template("detail.html", datetime=datetime)

def get_image(url):
	'''image_file = download_file('ftp://ftp.asc-csa.gc.ca/users/OpenData_DonneesOuvertes/pub/NEOSSAT/ASTRO/2018/284/TOI129/FINE_POINT/NEOS_SCI_2018284225800.fits')
	image_data = fits.getdata(image_file, ext=0)
	image_plt = plt.imshow(image_data, cmap='gray')'''

if __name__ == '__main__':
	app.run(debug=True)