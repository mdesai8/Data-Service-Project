from flask import Flask, request
from flask_restplus import Resource, Api
from flask_cors import CORS
from Models.Authentication import Authentication
from Models.Usage import Usage

app = Flask(__name__)
CORS(app)
api = Api(app)
usage = Usage(0)
auth = Authentication(False)
