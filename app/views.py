from flask import Flask, render_template, request

from .utils.parser import Parser
from .utils.api_getter import ApiGetter

app = Flask(__name__)

app.config.from_object('config')

@app.route('/')
def index():
    """The main page of the app"""
    return render_template("index.html")

@app.route("/get_answer")
def get_answer():
    """Fetch an answer to the user question"""
    user_message = request.args.get("user_message")
    parsed_message = Parser().parse(user_message)
    return ApiGetter().main(parsed_message)

if __name__ == "__main__":
    app.run()
