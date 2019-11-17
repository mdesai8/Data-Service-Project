from flask import Flask, request
from flask_restplus import Resource, Api
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
api = Api(app)

class Usage():
    def __init__(self, api_calls):
        self.api_calls = api_calls

    def get_usage(self):
        calls = self.api_calls
        return calls

    def inc_usage(self):
        self.api_calls += 1

class Authentication():
    def __init__(self, is_logged_in):
        self.is_logged_in = is_logged_in

    def check_auth(self):
        return self.is_logged_in

    def set_auth(self, logged, uid):
        self.is_logged_in = logged
        self.uid = uid

# Only used for API provider, not be given to consumer
@api.route("/authentication")
class Auth(Resource):
    @api.response(200, 'Authenticated')
    @api.response(400, 'Invalid Credentials')
    def post(self):
        body = request.json
    
        if body['username'] == 'user' and body['password'] == 'password':
            auth.set_auth(True, 'user')
            print(auth.check_auth())
            return {"message": "Success"}, 200

        else:
            print(auth.check_auth())
            return {"message": "Invalid Credentials"}, 400

if __name__ == "__main__":
    usage = Usage(0)
    auth = Authentication(False)
    app.run(debug=True)