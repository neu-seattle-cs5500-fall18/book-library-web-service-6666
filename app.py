from flask import Flask
app = Flask(__name__)

@app.route("/")
def home():
    return "Team 6666"
