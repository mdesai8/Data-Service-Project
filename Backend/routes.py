from server import *
from Predictors.LiteracyPredictor import *
import json

@api.route("/authentication")
class Auth(Resource):
    @api.response(200, 'Authenticated')
    @api.response(400, 'Invalid Credentials')
    def post(self):
        body = request.json

        if body['username'] == 'user' and body['password'] == 'password':
            auth.set_auth(True, 'user')
            # print(auth.check_auth())

            plt_line = plotRatePerCountryImputed(29)
            plt_bar = plotYearBar(2022)

            return {"bar_x": json.dumps(plt_bar[0].tolist()),
                    "bar_y": json.dumps(plt_bar[1].tolist()),
                    "message": "Success",
                    "x": json.dumps(plt_line[0].tolist()),
                    "y": json.dumps(plt_line[1].tolist())}, 200

        else:
            print(auth.check_auth())
            return {"message": "Invalid Credentials"}, 400
