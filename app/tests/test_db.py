
import pytest
from app.config import Config

def test_DB(db):
    from mongomock import MongoClient
    from app.db import DB

    assert isinstance(db, DB)
    assert isinstance(db.client, MongoClient)

def test_Document(db):
    from pymongo.results import InsertOneResult
    from pydantic import BaseModel
    from pydantic import ValidationError
    from app.db import DB, Document

    class TestClass(Document): pass

    with pytest.raises(TypeError, match="Can't instantiate abstract class TestClass without an implementation for abstract methods 'collection', 'model'"): 
        TestClass()

    del TestClass

    class TestModel(BaseModel):
        test_field: str

    class TestClass(Document):
        collection = DB().get_collection('test')
        model = TestModel

        def __init__(self, data: dict):
            self.data = data

        @classmethod
        def from_query(cls, query: dict):
            data = cls.collection.find_one(query)

            return TestClass(data=data)

    doc = TestClass(data={'x': 1})

    with pytest.raises(ValidationError):
        doc.commit()

    doc = TestClass(data={'test_field': 'value'})
    result = doc.commit()
    assert isinstance(result, InsertOneResult)
    _id = doc.data.get('_id')
    doc = TestClass.from_query({'_id': _id})
    assert doc.data['_id'] == _id

def test_User(db):
    from app.db import Document, User

    user = User(data={'name': 'testuser'})
    assert issubclass(User, Document)
    user.update_password()
    user.login()




     

