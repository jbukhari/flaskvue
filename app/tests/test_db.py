
import pytest
from mongomock import MongoClient
from app.config import Config

def test_db(db):
    from app.db import DB

    assert isinstance(db, DB)
    assert isinstance(db.client, MongoClient)

def test_interface(db):
    from app.db import Collection, Document

    collection = db.database.get_collection('test')
    collection.insert_one({'_id': 1})
    Collection.name = 'test'
    Collection.collection = collection
    item = Collection.find_one({'_id': 1})
    assert isinstance(item, Document)

def test_users(db):
    from app.db import Users

    assert Users.find_one({'name': 'foo'}) is None
    Users.add_user('foo')
    user = Users.find_one({'name': 'foo'})
    assert user.get('name') == 'foo'
    assert user.get('password') is None

     

