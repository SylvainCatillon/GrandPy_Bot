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
    result = api_getter.main()
    if result:
        grandpy_sentence = "Comment?! {name}? Ahhhh, oui, je me souviens de cette adresse! c'est: {address}"
        grandpy_story = "Mais t'ai-je déjà raconté l'histoire de ce quartier qui m'a vu en culottes courtes ? {story_title}: {story}"
        return {
            "status": "OK",
            "address":  grandpy_sentence.format(**result),
            "static_map_url": result["static_map_url"],
            "story": grandpy_story.format(**result)}
    else:
        return {
            "status": "address_not_found",
            "message": "Désolé mon p'tit, je me souviens plus où c'est..."}

if __name__ == "__main__":
    app.run()