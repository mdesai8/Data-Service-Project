# from server import *
from flask import Flask, request, send_file
from flask_restplus import Resource, Api
from flask_cors import CORS, cross_origin
# from Predictors.LiteracyPredictor import *
from flask import request
from flask_restplus import fields
from lifeexpec_predict import *
from predictCO2 import *
from gdp_predict import *
from predictFertility import *
from labour_predict import *
from track_usage import *
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

        if p_le == False:
            return {"message": "Country does not exist"}, 404

        with open("predicted_images/life_expec.png", "rb") as imageFile:
            encoded_image = str(base64.b64encode(imageFile.read()))[2:]
            encoded_image = encoded_image[:-1]

            incrementUsage('life_expectancy')
            numCalls = getNumUsages('life_expectancy')

            return {"predicted_value": p_le,
                    "num_calls" : numCalls,
                    "image": "data:image/png;base64,"+encoded_image}, 200


@api.route("/gdp_endpoint")
class Predict_gdp(Resource):
    @api.response(200, "Successful")
    @api.response(404, "Country name does not exist")
    @api.response(400, "Malformed Request")
    @api.doc(description="Obtain the predicted GDP of a country for a particular year")
    @api.expect(input_model, validate=True)
    def post(self):
        body = request.json

        if 'year' not in body or 'country_name' not in body:
            return {"message": "No year or country provided"}, 400

        country = body['country_name']
        year = body['year']
        predicted_gdp = gdp_predicted(country, year)

        if predicted_gdp == False:
            return {"message": "Country does not exist"}, 404

        predicted_gdp = str(predicted_gdp)
        predicted_gdp = predicted_gdp+" US$"

        with open("predicted_images/gdp.png", "rb") as imageFile:
            encoded_image = str(base64.b64encode(imageFile.read()))[2:]
            encoded_image = encoded_image[:-1]

            incrementUsage('gdp')
            numCalls = getNumUsages('gdp')

            return {"predicted_value": predicted_gdp,
                    "num_calls" : numCalls,
                    "image": "data:image/png;base64,"+encoded_image}, 200

@api.route("/labour")
class Labour(Resource):
    @api.response(200, "Successful")
    @api.response(404, "Country name does not exist")
    @api.response(400, "Malformed Request")
    @api.doc(description="Obtain the predicted labour force of a country for a particular year")
    @api.expect(input_model, validate=True)
    def post(self):
        body = request.json

        if 'year' not in body or 'country_name' not in body:
            return {"message": "No year or country provided"}, 400

        country = body['country_name']
        year = body['year']
        labourPred = predicted_labour(country, year)

        if labourPred == False:
            return {"message": "Country does not exist"}, 404

        labourPred=str(labourPred)

        with open("predicted_images/labour.png", "rb") as imageFile:
            encoded_image = str(base64.b64encode(imageFile.read()))[2:]
            encoded_image = encoded_image[:-1]

            incrementUsage('labour')
            numCalls = getNumUsages('labour')

            return {"predicted_value": labourPred,
                    "num_calls" : numCalls,
                    "image": "data:image/png;base64,"+encoded_image}, 200

@api.route("/co2_emission")
#@cross_origin()
class CO2_Emission(Resource):
    @api.response(200, "Successful")
    @api.response(404, "Country name does not exist")
    @api.response(400, "Malformed Request")
    @api.doc(description="Obtain the predicted CO2 Emission of a country for a particular year")
    @api.expect(input_model, validate=True)
    def post(self):
        body = request.json


        if 'year' not in body or 'country_name' not in body:
            return {"message": "No year or country provided"}, 400

        country = body['country_name']
        year = body['year']
        predictedEmission = predictCO2(country, year)

        if predictedEmission == False:
            return {"message": "Country does not exist"}, 404

        with open("predicted_images/CO2Emission.png", "rb") as imageFile:
            encoded_image = str(base64.b64encode(imageFile.read()))[2:]
            encoded_image = encoded_image[:-1]

            incrementUsage('co2')
            numCalls = getNumUsages('co2')

            return {"predicted_value": predictedEmission,
                    "num_calls" : numCalls,
                    "image": "data:image/png;base64,"+encoded_image}, 200

@api.route("/fertility_rate")
#@cross_origin()
class Fertility_Rate(Resource):
    @api.response(200, "Successful")
    @api.response(404, "Country name does not exist")
    @api.response(400, "Malformed Request")
    @api.doc(description="Obtain the predicted Fertility rate of a country for a particular year")
    @api.expect(input_model, validate=True)
    def post(self):
        body = request.json


        if 'year' not in body or 'country_name' not in body:
            return {"message": "No year or country provided"}, 400

        country = body['country_name']
        year = body['year']
        predictedFertility = pred_fertility(country, year)

        if predictedFertility == False:
            return {"message": "Country does not exist"}, 404

        with open("predicted_images/FertilityRate.png", "rb") as imageFile:
            encoded_image = str(base64.b64encode(imageFile.read()))[2:]
            encoded_image = encoded_image[:-1]

            incrementUsage('fertility_rate')
            numCalls = getNumUsages('fertility_rate')

            return {"predicted_value": predictedFertility,
                    "num_calls" : numCalls,
                    "image": "data:image/png;base64,"+encoded_image}, 200



if __name__ == "__main__":
    auth = Authentication(False)
    usage = Usage(0)
    app.run(debug=True)
