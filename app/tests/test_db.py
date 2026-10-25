
import pytest
from app.config import Config

def test_db(db):
    from mongomock import MongoClient
    from app.db import DB

    assert isinstance(db, DB)
    assert isinstance(db.client, MongoClient)  

def test_user(db):
    from mongomock import Collection
    from pymongo.results import UpdateResult
    from app.db import User

    # commit
    user = User(name='testuser')
    assert isinstance(user.collection, Collection)
    result = user.commit()
    assert isinstance(result, UpdateResult)
    assert result.acknowledged
    assert user.collection

    # delete



     

