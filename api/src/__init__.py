from flask import Flask
from flask_cors import CORS
from flask_restful import Api
from .urls import initialize_urls

app = Flask(__name__)
CORS(app)
api = Api(app)
initialize_urls(api)
