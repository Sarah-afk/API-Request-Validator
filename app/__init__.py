from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

directory = os.getcwd()
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///{}/database.db".format(directory)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

app.secret_key = "Task"

from app.routes import *
from app.models import *

initalize_db()