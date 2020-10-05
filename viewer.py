import io
import base64

from flask import Flask, Response, render_template, request, redirect, url_for
from functions import Images, Spectral

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


@app.route('/', methods=["POST", "GET"])
def view():
	if request.method == "POST":
		type = str(request.form["type"])
		waveBand = str(request.form["waveBand"])
		keyword = str(request.form["keyword"])
		coord = str(request.form["coord"])
		size = float(request.form["size"])

		if type == "ssa" and waveBand == "x-ray":
			spe = Spectral(type, waveBand, keyword, coord, size)
			img_url = " "
			url = spe.getSpectral()
		elif type == "image" and (waveBand == "uv" or "optical"):
			img = Images(type, waveBand, keyword, coord, size)
			img_url = img.getUltravioletUrl()
			url = img.getUltravioletFits()
		else:
			img_url = " "
			url = "null"

		return render_template("search-results.html", jpg_url=img_url)
	else:
		all_xml_dict = []

		manual_urls = [
			"ftp://data.asc-csa.gc.ca/users/OpenData_DonneesOuvertes/pub/NEOSSAT/XML/NEOS_SCI_2018284225800-2018-10-15-02-00-25.xml",
			"ftp://data.asc-csa.gc.ca/users/OpenData_DonneesOuvertes/pub/NEOSSAT/XML/NEOS_SCI_2018251042635-2018-10-15-01-59-42.xml",
			"ftp://data.asc-csa.gc.ca/users/OpenData_DonneesOuvertes/pub/NEOSSAT/XML/NEOS_SCI_2018232040619-2018-10-15-10-49-24.xml",
			"ftp://data.asc-csa.gc.ca/users/OpenData_DonneesOuvertes/pub/NEOSSAT/XML/NEOS_SCI_2018033164500-2018-10-15-12-54-57.xml",
			"ftp://data.asc-csa.gc.ca/users/OpenData_DonneesOuvertes/pub/NEOSSAT/XML/NEOS_SCI_2017283104140-2018-10-15-12-49-38.xml"]

		for url in manual_urls:
			response = urllib.request.urlopen(url).read()
			data = xmltodict.parse(response, dict_constructor=dict)
			all_xml_dict.append(data)

	return render_template("viewer.html", message="message", test_obj=all_xml_dict)

@app.route('/about')
def about():
	return render_template("about.html")

if __name__ == '__main__':
	app.run(debug=True)
