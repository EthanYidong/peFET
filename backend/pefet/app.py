from flask import Flask

from peewee import SqliteDatabase

app = Flask(__name__)
app.config.from_object('config.Configuration')

db = SqliteDatabase(app.config['DATABASE'])
