from flask import Flask, render_template

app = Flask(__name__,
            template_folder="templates",
            static_folder="static")

@app.route("/")
def index():
    # code here ROFLMAO