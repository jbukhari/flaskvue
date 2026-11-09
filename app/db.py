# All direct interaction with the database can be done here using subclasses of
# the Document abstract base class.

import sys, os
from warnings import warn
from abc import ABCMeta, abstractmethod
from typing import Self
from collections.abc import Iterable
from dataclasses import dataclass
from pymongo import MongoClient, CursorType
from pymongo.database import Database as DatabaseHandle
from pymongo.collection import Collection
from pymongo.results import InsertOneResult, UpdateResult
from bson.objectid import ObjectId
from mongomock import MongoClient as MockClient, Collection as MockCollection
from pydantic import BaseModel
from flask_login import UserMixin, login_user
from werkzeug.security import generate_password_hash, check_password_hash
from app.config import Config
from app import models

DBVAR = 'DATABASE_CONNECTION_STRING'

class Identifier():
    def __init__(self, *, field: str, value=None):
        self.field = field
        self.value = value

class DB():
    """Interface to the database."""

    def __init__(self):
        f"""Connects to the database using the connection string provided by
        the environment variable "{DBVAR}", if it exists. Otherwise connect to
        a Mongomock DB"""
        
        self.connected = False

        if connect := os.environ.get(DBVAR):
            self.client = MongoClient(connect)
        elif 'pytest' in sys.modules:
            self.client = MockClient()
        else:
            warn(f'Environment variable "{DBVAR}" not found. Connecting to Mongomock database"')
            self.client = MockClient()

        self.database: DatabaseHandle = self.client.get_database(Config.DATABASE_NAME)
   
    def get_collection(self, name: str) -> Collection:
        """Utility for getting a collection handle by name"""
    
        return DB().database.get_collection(name) if name else None

@dataclass
class Document(metaclass=ABCMeta):
    """Abstract base class representing a single database document"""

    @property
    @abstractmethod
    def collection(self) -> Collection: pass

    @property
    @abstractmethod
    def model(self) -> type[BaseModel]: pass

    data: Iterable

    def __post_init__(self):
        assert isinstance(self.collection, (Collection, MockCollection))
        assert models.Base in self.model.__bases__

    @classmethod
    def from_query(cls, query: dict) -> Self | None:
        if not query: return None

        if data := cls.collection.find_one(query):
            return cls(data)

    def commit(self) -> InsertOneResult | UpdateResult:
        if not hasattr(self, 'data') or self.data is None:
            raise Exception('Attribute "data" not set')

        self.model(**self.data)
        to_commit = {k: self.data[k] for k in self.model.model_fields if k in self.data}
        
        if _id := self.data.get('_id'):
            q = {'_id': _id}
            result = self.collection.replace_one(q, to_commit)
        else:
            result = self.collection.insert_one(to_commit)
            self.data['_id'] = result.inserted_id

        return result

    #@abstractmethod
    def delete(self) -> Self: pass

### User system

class User(Document, UserMixin):
    """Interface to single document in collection "users". Inherits from
    the Flask-Login UserMixin class, so instances can be used to log in the
    user represented by the document"""

    collection: Collection = DB().get_collection('users')
    model: type[BaseModel] = models.User

    @classmethod
    def add_user(cls, user_id: str, password: str) -> Self:
        if cls.collection.find_one({'userId': user_id}):
            raise Exception(f'User "{user_id}" already exists')

        self = cls(data={'userId': user_id, 'passwordHash': generate_password_hash(password)})
        super(cls, self).commit()

        return self
    
    def get_id(self) -> str:
        return self.data.get('userId')

    def commit(self) -> InsertOneResult | UpdateResult:
        if self.data.get('_id') is None:
            raise Exception('Can\'t add new user to the database with `User.commit`. Use `User.add_user`')
        elif existing := self.collection.find_one({'_id': self.data['_id']}):
            if self.data.get('password_hash') != existing['password_hash']:
                raise Exception('Can\'t change password with `User.commit`. Use `User.update_password`')

        return super().commit()

    def update_password(self, new_password: str) -> InsertOneResult | UpdateResult:
        self.data['passwordHash'] = generate_password_hash(new_password)
        
        return super().commit()

    def login(self, password: str) -> bool:
        if self.data.get('_id') is None:
            raise Exception('User is not in the system')

        if not check_password_hash(self.data['passwordHash'], password):
            return False
        
        return login_user(self)
    
