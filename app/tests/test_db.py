
from datetime import datetime

import pytest

from app.config import Config


def test_DB(db):
    from mongomock import MongoClient

    from app.db import DB

    assert isinstance(db, DB)
    assert isinstance(db.client, MongoClient)

def test_Document(db):
    from pydantic import ValidationError
    from pymongo.results import InsertOneResult, UpdateResult

    from app.db import Document
    from app.models import Base

    with pytest.raises(TypeError, match="Can't instantiate abstract class"):
        Document()

    class TestClass(Document): pass

    with pytest.raises(TypeError, match="Can't instantiate abstract class"):
        TestClass()

    del TestClass

    class TestModel(Base):
        test_field: str

    class TestClass(Document):
        collection = db.get_collection('testDocs')
        model = TestModel

    with pytest.raises(ValidationError):
        TestClass(data={'x': 1}).commit()

    doc = TestClass(data={'test_field': 'value'})
    result = doc.commit()
    assert isinstance(result[0], InsertOneResult)
    assert isinstance(result[1], UpdateResult)
    _id = doc.data.get('_id')
    retrieved = TestClass.from_query({'_id': _id})
    assert retrieved.data['_id'] == _id
    def get_audit(__id, /): return retrieved.audit_collection.find_one({'_id': __id})
    audit1 = get_audit(_id)
    assert audit1['history'][0]['data'] == retrieved.data
    retrieved.data['test_field'] = 'updated'
    retrieved.commit()
    audit2 = get_audit(_id)
    assert isinstance(audit2['history'][1]['updated'], datetime)
    assert audit2['history'][1]['data']['test_field'] == 'updated'
    doc.delete()
    assert doc.data.get('_id') is None
    assert TestClass.from_query({'_id': _id}) is None
    audit3 = get_audit(_id)
    assert isinstance(audit3['deleted'], datetime)
   
def test_User(client, db):
    from flask_login import UserMixin
    from pymongo.results import UpdateResult
    from werkzeug.security import check_password_hash

    from app.db import Document, User
    
    User.collection = db.client.get_database(Config.DATABASE_NAME).get_collection('users')

    with pytest.raises(Exception, match="Can't add new user to the database with `User.commit`"):
        User({'userId': 'x'}).commit()

    assert isinstance(User.add_user('test', 'pw'), Document | User | UserMixin)
    user = User.from_query({'userId': 'test'})
    hash = user.data['passwordHash']
    assert check_password_hash(hash, 'pw')

    with pytest.raises(Exception, match="Can't change password with `User.commit`"):
        user.data['passwordHash'] = 'illegal'
        user.commit()

    result = user.update_password('new_pw')
    assert all(isinstance(x, UpdateResult) for x in result)
    new_hash = user.data['passwordHash'] 
    assert new_hash != hash
    assert check_password_hash(new_hash, 'new_pw')

    with pytest.raises(RuntimeError, match='Working outside of application context'):
        user.login('new_pw')

    assert client.post('/login', data={'userId': '', 'password': ''}).status_code == 404
    assert client.post('/login', data={'userId': 'test', 'password': 'pw'}).status_code == 401
    assert client.post('/login', data={'userId': 'test', 'password': 'new_pw'}).status_code == 302