import text
from app.stopwords_fr import stopwords_list

try:
    from instance import config as instance_config
except ImportError:
    instance_config = None


if instance_config:
    GOOGLE_API_KEY = instance_config.GOOGLE_API_KEY
else:
    GOOGLE_API_KEY = ""

TEXT = text.fr_text

START_KEYWORDS = ["adresse", "où", "l'adresse"]
END_KEYWORDS = ["?", ".", "!", ";"]
STOPWORDS = stopwords_list+["grandpy", "bot", "grandpybot"]