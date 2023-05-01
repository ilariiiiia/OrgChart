from os.path import join, dirname, realpath
from werkzeug.utils import secure_filename
import os


def saveFile(request, _file):
	UPLOADS_PATH = join(dirname(realpath(_file)), 'static/userdata/')
	n = len([name for name in os.listdir(UPLOADS_PATH) if os.path.isfile(name)])
	if request.method == 'POST':
		if 'file' not in request.files:
			return "Wrong one little boy"
		file = request.files['file']
		if file and file.filename:
			filename = secure_filename(file.filename)
			file.save(UPLOADS_PATH + filename)
			return hex(n + 1234)
	return '''<h1>Something went wrong!</h1>'''