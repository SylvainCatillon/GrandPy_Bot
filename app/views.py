from flask import Flask, render_template, request

from instance import config as instance_config
from .utils import Parser, ApiGetter

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")

@app.route("/getResponse")
def getResponse():
    user_message = request.args.get("user_message")
    parsed_message = Parser().parse(user_message)
    api_getter = ApiGetter(instance_config.GOOGLE_API_KEY, parsed_message)
    address, static_map_url, name = api_getter.main()
    grandpy_sentence = "Comment?! {name}? Ahhhh, oui, je me souviens de cette adresse! c'est: {address}"
    return {
        "address":  grandpy_sentence.format(name=name, address=address),
        "static_map_url": static_map_url}

if __name__ == "__main__":
    app.run()