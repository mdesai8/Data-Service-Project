# from server import app
from flask import render_template
from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
# CORS(app)
# api = Api(app)

@app.route("/")
def home():
    return render_template('home.html')

if __name__ == "__main__":
    app.run(debug=True,port=8321)