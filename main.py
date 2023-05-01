from utils.treeParser import TreeParser
from utils.html import renderTribes, choiceHTML
from utils.save import saveFile

from flask import Flask, request

t = TreeParser('employees.csv')

app = Flask(__name__)

css = open('static/global.css').read()

@app.route("/")
def index():
	return open('static/index.html').read()

@app.route("/view")
def view():
	hide = "<script type='text/javascript'>let selected = document.querySelector('select').value;document.querySelectorAll('.allWrapper').forEach((it) => {it.id === selected ? it.style.display = 'flex' : it.style.display = 'none';})</script>"
	return f"<style>{css}</style>{choiceHTML(t.tribes)}<div class='tribesWrapper'>{renderTribes(t.tribes)}</div>{hide}"

@app.route('/submitFile', methods=['POST'])
def upload_file():
	return saveFile(request, __file__)

if __name__ == "__main__":
  app.run(host="0.0.0.0", port=8080, debug=True)