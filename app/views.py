from flask import Flask, render_template, request

from instance import config as instance_config
from .utils import Parser, ApiGetter

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")

@app.route("/get_response")
def get_response():
    user_message = request.args.get("user_message")
    parsed_message = Parser().parse(user_message)
    # Changer API key!
    api_getter = ApiGetter(instance_config.GOOGLE_API_KEY, parsed_message)
    return api_getter.main()

if __name__ == "__main__":
    app.run()