from flask import Flask, render_template, request

from .utils.Parser import Parser
from .utils.ApiGetter import ApiGetter

app = Flask(__name__)

app.config.from_object('config')

@app.route('/')
def index():
    return render_template("index.html")

@app.route("/get_response")
def get_response():
    user_message = request.args.get("user_message")
    parsed_message = Parser().parse(user_message)
    return ApiGetter().main(parsed_message)

if __name__ == "__main__":
    app.run()