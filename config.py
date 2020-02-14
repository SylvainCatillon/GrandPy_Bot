import text
try:
    from instance import config as instance_config
except ImportError:
    instance_config = None

TEXT = text.fr_text
if instance_config:
    GOOGLE_API_KEY = instance_config.GOOGLE_API_KEY
else:
    GOOGLE_API_KEY = ""