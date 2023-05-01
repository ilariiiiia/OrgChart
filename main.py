from utils.treeParser import TreeParser
from utils.html import renderTribes, choiceHTML

from flask import Flask

t = TreeParser('employees.csv')

app = Flask(__name__)

css = open('static/global.css').read()

@app.route("/")
def index():
	# definitely not the way to do it, but it definitely also works
	hide = "<script type='text/javascript'>let selected = document.querySelector('select').value;document.querySelectorAll('.allWrapper').forEach((it) => {it.id === selected ? it.style.display = 'flex' : it.style.display = 'none';})</script>"
	return f"<style>{css}</style>{choiceHTML(t.tribes)}<div class='tribesWrapper'>{renderTribes(t.tribes)}</div>{hide}"

if __name__ == "__main__":
  app.run(host="0.0.0.0", port=8080, debug=False)