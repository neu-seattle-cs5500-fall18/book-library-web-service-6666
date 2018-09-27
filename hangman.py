from flask import Flask
from flask import jsonify
import random
app = Flask(__name__)

# pool = ["apple", "orange", "pear", "grape"]
# word = ""
# guessed = []
# known = []

@app.route("/")
def home():
    return "hello world!"

# @app.route("/start")
# def start():
#     global word, known
#     word = random.choice(pool)
#     known = []
#     for i in range(len(word)):
#         known.append("")
#     return str(known)
#
#
# @app.route("/guess")
# def guess(letter):
#     return "Hello World!"
