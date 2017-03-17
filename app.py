from flask import Flask, render_template, url_for, request, session, redirect
from flask_session import Session

app = Flask(__name__)
sess = Session()


@app.route("/")
def index():
	return render_template("index.html")


app.secret_key = 'kwoc'
app.config['SESSION_TYPE'] = 'filesystem'

sess.init_app(app)
app.debug = True

if __name__ == "__main__" :
	app.run(debug=True)