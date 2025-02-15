import re, time
from os import environ
 

id_pattern = re.compile(r'^.\d+$')

def is_enabled(value, default):
    if value.strip().lower() in ["on", "true", "yes", "1", "enable", "y"]: return True
    elif value.strip().lower() in ["off", "false", "no", "0", "disable", "n"]: return False
    else: return default


DATABASE_NAME = environ.get('DATABASE_NAME', "Mrsyd")
DATABASE_URL = environ.get('DATABASE_URL', "")
API_URL = environ.get('API_URL', "")
API_URI = environ.get('API_URI', "")
NUMB = environ.get('NUMB', "")
auth_channel = environ.get('AUTH_CHANNEL', '')
AUTH_CHANNEL = int(auth_channel) if auth_channel and id_pattern.search(auth_channel) else None
