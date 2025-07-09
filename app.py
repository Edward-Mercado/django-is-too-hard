from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def home():
    return render_template('index.html')
@app.route("/city/city")
def city_home():
    return render_template('test.html')