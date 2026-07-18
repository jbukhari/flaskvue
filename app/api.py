# API routes defined using Flask-RESTX and imported into the main app via
# Blueprint.

import json
from flask import abort, request, jsonify, Response, Blueprint
from flask_restx import Api, Namespace, Resource, fields
from flask_pydantic import validate
from app import models

API = Api(Blueprint('api', __name__), version='1.0', doc='/')
NS = API.namespace('v1')

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