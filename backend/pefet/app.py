import logging

from flask import Flask
from flask_cors import CORS

from peewee import SqliteDatabase

app = Flask(__name__)

logging.basicConfig(level=logging.DEBUG)

# To enable logging for flask-cors,
logging.getLogger('flask_cors').level = logging.DEBUG

# TODO: add stricter CORS restrictions
CORS(app, send_wildcard=True)
app.config.from_object('config.Configuration')

db = SqliteDatabase(app.config['DATABASE'])
