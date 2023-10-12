import pathlib

BASE_DIR = pathlib.Path(__file__).parent.parent

WEBHOOK_SECRET_TOKEN = "CONNECTFOURBYLEROYBIT"
BOT_TOKEN = ""

BASE_URL = "https://example.com"
WEBHOOK_PATH = '/' + BOT_TOKEN 
MINI_APP_NAME = ''
SSL_CERT = '' # leave empty if you want run server as http
SSL_PRIVATE_KEY = '' # leave empty if you want run server as http

LOG_LEVEL = 'INFO' # TRACE, DEBUG, INFO, WARNING, ERROR, CRITICAL
       
