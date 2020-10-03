from flask import Flask, render_template

import urllib.request
import xmltodict
import ftplib

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

			for filename in filenames:
				if "2015" in filename and iterations < 5 :
					iterations += 1
					url = 'ftp://data.asc-csa.gc.ca/users/OpenData_DonneesOuvertes/pub/NEOSSAT/XML/' + filename
					response = urllib.request.urlopen(url).read()
					data = xmltodict.parse(response)
					all_xml_dict.append(data)
				if iterations is 5:
					print(all_xml_dict[0]['FITSImage']['Attitude'])
					break

		except ftplib.all_errors as e:
			print('FTP error:', e)

	return render_template("viewer.html", message="message", test_obj=all_xml_dict)

if __name__ == '__main__':
	app.run(debug=True)