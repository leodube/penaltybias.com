from flask import Flask 
from flask_restful import Api
from .api.urls import initialize_urls

app = Flask(__name__)
api = Api(app)
initialize_urls(api)
