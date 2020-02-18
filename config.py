import os

import text
from app.stopwords_fr import STOPWORDS_LIST

#  Try to import instance config if it exists
try:
    from instance import config as instance_config
except ImportError:
    instance_config = None


#  Get GOOGLE_API_KEY from instance config if it exists
if instance_config:
    GOOGLE_API_KEY = instance_config.GOOGLE_API_KEY
#  Get GOOGLE_API_KEY from environment, with an empty string as default
else:
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "")

#  The sentences to be used in the program
TEXT = text.FR_TEXT

#  The starting and ending keywords to find an address in the user question
START_KEYWORDS = ["adresse", "où", "l'adresse"]
END_KEYWORDS = ["?", ".", "!", ";"]

#  The words to delete from the user question
STOPWORDS = STOPWORDS_LIST+["grandpy", "bot", "grandpybot"]
