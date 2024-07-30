import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL", "postgresql://ufcdle_user:U3yqLBsJXcB0FPVvshzAJcM8bDdnLtzU@dpg-cqhhpo56l47c73fnr7qg-a.ohio-postgres.render.com/ufcdle")
#postgresql://ufcdle_user:U3yqLBsJXcB0FPVvshzAJcM8bDdnLtzU@dpg-cqhhpo56l47c73fnr7qg-a.ohio-postgres.render.com/ufcdle

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)