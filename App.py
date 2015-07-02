from flask import *
from flask_cors import CORS
from flask_httpauth import HTTPBasicAuth
from flask_restful import Resource, reqparse, Api
from werkzeug.exceptions import HTTPException

# Flask App
appObj = Flask(__name__, static_url_path="")

# Allowed cross origin support
CORS(appObj, resources={'/api/v1/*': {"origins": "*"}})
apiObj = Api(appObj)

def CreateResponse(responseCode, responseMessage, responseObject=None):
    _response = {'status': responseCode, 'message': responseMessage}
    if responseObject:
        _response.update({'data': responseObject})
    return make_response(jsonify(_response), responseCode)

class ApiList(Resource):
    def __init__(self):
        super(ApiList, self).__init__()

    def get(self):
        endpoint = []
        for _endpoint in apiObj.app.url_map._rules:
            endpoint.append(_endpoint.rule)
        return CreateResponse(200, 'Success', sorted(endpoint))

class Heartbeat(Resource):
    def __init__(self):
        super(Heartbeat, self).__init__()

    def get(self):
        return make_response('', 204)

apiObj.add_resource(Heartbeat, '/api/v1/heartbeat', endpoint='Heartbeat')
apiObj.add_resource(ApiList, '/api/v1', endpoint='API')

if __name__ == '__main__':
    appObj.run(debug=False,
               threaded=True,
               port=12345,
               host='0.0.0.0')