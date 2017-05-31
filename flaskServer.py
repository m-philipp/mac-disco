from flask import Flask, redirect, url_for

app = Flask(__name__)

@app.route('/')
def index():
	return redirect(url_for('static', filename='index.html'))

@app.route('/saveName')
def saveName():
	return "saved"

if __name__ == "__main__":
	app.run(host='0.0.0.0', port=8080, debug=True)
