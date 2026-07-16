# Models are defined as Pydantic models but can be converted to Flask-RESTX
# model objects using the provided methods.

from pydantic import BaseModel
from flask_restx import Api, fields
from flask_restx.model import Model, SchemaModel

### Base

class Base(BaseModel):
    """Adds methods to Pydantic base class for converting Pydantic models to
    Flask-RESTX models"""

    @classmethod
    def jsonschema(cls) -> str:
        """Returns the JSON Schema representation of the model as a JSON string"""
        return cls.model_json_schema()
    
    @classmethod
    def schema_model(cls) -> SchemaModel:
        """Returns the model as a Flask-RESTX SchemaModel"""
        from app.api import API
        
        return API.schema_model('Record', cls.jsonschema())
    
    @classmethod
    def model(cls) -> Model:
        """Returns the model as a Flask-RESTX model"""
        from app.api import API

        type_map = {
            # Map of JSON Schema data types to Flask-RESTX types
            "boolean": fields.Boolean,
            "integer": fields.Integer,
            "string": fields.String,
            "array": fields.List,
            "object": fields.Nested
        }
        data = {}

        for prop, config in cls.jsonschema().get('properties').items():
            data[prop] = type_map[config['type']]
        
        return API.model('Record', data)
    
### Models

class Record(Base):
    id: int
