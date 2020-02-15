import text
from app.stopwords_fr import STOPWORDS_LIST

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
STOPWORDS = STOPWORDS_LIST+["grandpy", "bot", "grandpybot"]
