from app import app, db

from models import *
from api import *


def create_tables():
    db.create_tables([User], safe=True)


if __name__ == '__main__':
    create_tables()
    app.run(host="0.0.0.0", port=8000)
