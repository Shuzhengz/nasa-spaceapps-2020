from flask import Flask, render_template

import xml.etree.ElementTree as ET
import urllib.request
import xmltodict

app = Flask(__name__)

@app.route('/')
def view():
	url = 'ftp://data.asc-csa.gc.ca/users/OpenData_DonneesOuvertes/pub/NEOSSAT/XML/NEOS_SCI_2015347000000-2018-10-15-12-29-28.xml'
	response = urllib.request.urlopen(url).read()
	'''tree = ET.fromstring(response)'''
	data = xmltodict.parse(response)

	return render_template("viewer.html", message="message", test_obj=data)

if __name__ == '__main__':
	app.run(debug=True)