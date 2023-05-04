from os.path import join, dirname, realpath
from werkzeug.utils import secure_filename
import os
import json

def reject(msg: str):
	return {
		"success": False,
		"message": msg
	}

def accept(msg: str):
	return {
		"success": True,
		"message": msg
	}

def uploadPath(_file):
	return join(dirname(realpath(_file)), 'static/userdata/')

def checkFileExtension(request):
	if 'file' not in request.files:
		return False
	
	file = request.files['file']
	return '.' in file.filename and file.filename.rsplit('.', 1)[1].lower() == 'csv'

def check_csv_header(file):
	headeralt = b'\xef\xbb\xbfTeam Member,Competence,Team,Area,Function,Tribe,Competence Lead,Team Lead,Area Lead,Function Lead,Tribe Lead'
	header = b'Team Member,Competence,Team,Area,Function,Tribe,Competence Lead,Team Lead,Area Lead,Function Lead,Tribe Lead'
	for line in file.readlines():
		
		if not line:  # EOF
			print("EOF")
			return False

		print(line.strip())
		
		if line.strip() == header or line.strip() == headeralt:
			return True
	
	return False

def saveFile(request, _file):
	n = len(os.listdir('./static/userdata'))
	if request.method == 'POST':
		if 'file' not in request.files:
			return reject("File not sent!")
		file = request.files['file']
		if not checkFileExtension(request):
			return reject("File extension not valid!")
		if not check_csv_header(file):
			return reject("CSV doesn't contain valid headers")
		file.seek(0)
		if file and file.filename:
			filename = secure_filename(file.filename)
			with open(uploadPath(_file) + filename, 'wb') as f:
				content = file.read()
				content = content[3:] if content.startswith(b'\xef\xbb\xbf') else content
				f.write(content)
			saveId(n, uploadPath(_file) + filename)
			return accept(hex(n + 1234))
	return reject("Somthing else went wrong! (likely wrong HTTP method. Only POST is accepted)")

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
		json.dump(matches, file, indent=4)