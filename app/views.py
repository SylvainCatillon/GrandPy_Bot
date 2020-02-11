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
    found_address = api_getter.main()
    if found_address:
        address, static_map_url, name, story, story_title = found_address
        grandpy_sentence = "Comment?! {name}? Ahhhh, oui, je me souviens de cette adresse! c'est: {address}"
        grandpy_story = "Mais t'ai-je déjà raconté l'histoire de ce quartier qui m'a vu en culottes courtes ? {story_title}: {story}"
        return {
            "status": "OK",
            "address":  grandpy_sentence.format(name=name, address=address),
            "static_map_url": static_map_url,
            "story": grandpy_story.format(story=story, story_title=story_title)}
    else:
        return {
            "status": "address_not_found",
            "message": "Désolé mon p'tit, je me souviens plus où c'est..."}

if __name__ == "__main__":
    app.run()