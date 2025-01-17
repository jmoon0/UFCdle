import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL", "postgres://neondb_owner:4FKXNUgHO2Pq@ep-muddy-sun-a5ffe9up-pooler.us-east-2.aws.neon.tech/neondb?sslmode=require")

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
