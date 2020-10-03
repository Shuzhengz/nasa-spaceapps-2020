from flask import Flask
app = Flask(__name__)

@app.route('/')
def view():
    return 'NASA Spaceapps 2020 - Hey, What Are You Looking At?'

if __name__ == '__main__':
	app.run(debug=True)