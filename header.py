from flask import Flask, request, jsonify, make_response, json
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import uuid
import jwt
import datetime
from functools import wraps
from flask_cors import CORS

app = Flask(__name__)
cors = CORS(app)

# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://ccfpbbksnwqtac:c425a7dd3adb83f74509da57cda34d3ebe3ed68491e4a5b491a6ec6e529af1d9@ec2-3-218-149-60.compute-1.amazonaws.com:5432/d2b021vs0r799u'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SECRET_KEY'] = 'thisissecret'

db = SQLAlchemy(app)
migrate = Migrate(app, db)
jwt = JWTManager(app)
