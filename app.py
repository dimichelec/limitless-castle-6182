from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.config.from_pyfile('config.py')
db = SQLAlchemy(app)

@app.route("/")
def hello():
	return "Hello World!"


@app.route("/<name>")
def hello_name(name):
	return "Hello {}!".format(name)

	
@app.route('/submit', methods=['POST'])
def submit():
	text = request.form["paste"]
	text = text.encode("ascii", errors="ignore")

	paste = Paste(text, "Anonymous")

	db.session.add(paste)
	db.session.commit()

	print "added paste by %s with id %s" % (poster, paste.id)
	return render_template("success.html", id=paste.id)

	
if __name__ == "__main__":
	app.run()
