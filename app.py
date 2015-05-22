from flask import Flask, render_template, request, redirect, url_for, abort, session
import random

app = Flask(__name__)
app.config['SECRET_KEY'] = 'JDas8dj123e&&@0h';

@app.route('/')
def home():
	return render_template('index.html')

@app.route('/signup', methods=['POST'])
def signup():
	session['username'] = request.form['username']
	session['comment'] = request.form['comment']
	return redirect(url_for('message'))

@app.route('/message')
def message():
	if not 'username' in session:
		return abort(403)
	return render_template('message.html',
		username=session['username'], comment=session['comment'],
		random=''.join(random.choice('0123456789abcdef') for i in range(256))
	)


if __name__ == "__main__":
	app.debug = True
	app.run()
