from os.path import join, dirname, realpath
from werkzeug.utils import secure_filename
import os
import json

def uploadPath(_file):
	return join(dirname(realpath(_file)), 'static/userdata/')

def saveFile(request, _file):
	n = len([name for name in os.listdir(uploadPath(_file)) if os.path.isfile(name)])
	if request.method == 'POST':
		if 'file' not in request.files:
			return "Wrong one little boy"
		file = request.files['file']
		if file and file.filename:
			filename = secure_filename(file.filename)
			file.save(uploadPath(_file) + filename)
			saveId(n, uploadPath(_file) + filename)
			return hex(n + 1234)
	return '''<h1>Something went wrong!</h1>'''

def getFileFromId(id: int):
	with open("./static/matches.json", "r") as file:
		matches = json.load(file)
		return matches[id]

def saveId(id: int, filename):
	n = hex(id + 1234)
	with open("./static/matches.json", "r") as file:
		matches = json.load(file)
	matches[n] = filename
	with open("./static/matches.json", "w") as file:
		json.dump(matches, file)