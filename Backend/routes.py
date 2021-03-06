

######
# USE 'routes.py' IN ROOT FOLDER
######

# from server import *
from flask import Flask, request, send_file
from flask_restplus import Resource, Api
from flask_cors import CORS
# from Predictors.LiteracyPredictor import *
from flask import request
from flask_restplus import fields
from lifeexpec_predict import *
import json
import base64

class Authentication():
    def __init__(self, is_logged_in):
        self.is_logged_in = is_logged_in

    def check_auth(self):
        return self.is_logged_in

    def set_auth(self, logged, uid):
        self.is_logged_in = logged
        self.uid = uid

class Usage():
    def __init__(self, api_calls):
        self.api_calls = api_calls

    def get_usage(self):
        calls = self.api_calls
        return calls

    def inc_usage(self):
        self.api_calls += 1

app = Flask(__name__)
CORS(app)
api = Api(app,
        default="Country Stats",
        title="Country Statistics",
        description="This API provides a way to get various predictions about a country by year")

input_model = api.model('Country_and_Year', {
    'country_name': fields.String,
    'year': fields.Integer
})

@api.route("/authentication")
class Auth(Resource):
    @api.response(200, 'Authenticated')
    @api.response(400, 'Invalid Credentials')
    @api.doc(description="Authenticate User")
    def post(self):
        body = request.json

        if body['username'] == 'user' and body['password'] == 'password':
            auth.set_auth(True, 'user')

            return {"message": "Success"}, 200

        else:
            print(auth.check_auth())
            return {"message": "Invalid Credentials"}, 400

@api.route("/life_expectancy")
class Life_Expectancy(Resource):
    @api.response(200, "Successful")
    @api.response(404, "Country name does not exist")
    @api.response(400, "Malformed Request")
    @api.doc(description="Obtain the predicted life expectancy of a country for a particular year")
    @api.expect(input_model, validate=True)
    def post(self):
        body = request.json

        if 'year' not in body or 'country_name' not in body:
            return {"message": "No year or country provided"}, 400

        country = body['country_name']
        year = body['year']
        p_le = predicted_life_expec(country, year)

        with open("predicted_images/life_expec.png", "rb") as imageFile:
            encoded_image = str(base64.b64encode(imageFile.read()))[2:]
            encoded_image = encoded_image[:-1]

            return {"predicted_value": p_le, "image": "data:image/png;base64,"+encoded_image}, 200

if __name__ == "__main__":
    auth = Authentication(False)
    usage = Usage(0)
    app.run(debug=True)