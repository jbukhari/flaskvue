# API routes defined using Flask-RESTX and imported into the main app via
# Blueprint.

import json
from flask import abort, request, jsonify, Response, Blueprint
from flask_restx import Api, Resource, fields
from flask_pydantic import validate
from app import models

API = Api(Blueprint('api', __name__, url_prefix='/api'), doc='/')
NS = API.namespace('api', description='App API') # multiple namespaces can be added if api subsections are needed

# All routes defined below come after "/api", set as an attribute to the 
# blueprint.
@NS.route('/')
class Doc(Resource):
    @NS.doc(description='API Documentation')
    def get(self):
        # Placeholder for the Swagger doc provided by Flask-RESTX, set using
        # the "doc" argument to the Api object.
        return {'message': 'The documentation is supposed to be supplied here by Flask-RESTX.'}

@NS.route('/records')
class Records(Resource):
    @NS.doc(description='List records')
    def get(self):
        data = [{'id': 1}]
        return jsonify(data)
    
    @NS.doc(description='Create record')
    @NS.expect(models.Record.model())
    def post(self):
        data = json.loads(request.data)
        
        if models.Record.model_validate(data):
            return Response(status=201)
        
        abort(400)
    
@NS.route('/record')
class Record(Resource):
    @NS.doc(description='Get record')
    def get(self):
        data = {'id': 1}
        return (data)