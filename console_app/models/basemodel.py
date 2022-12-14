#!/usr/bin/env python3
"""
Contains the BaseModel class
"""
from datetime import datetime
from sqlalchemy import Column, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from uuid import uuid4
import models

Base = declarative_base()

class BaseModel():
    """Defines the BaseModel class.
    Attributes:
        id (sqlalchemy String): The BaseModel id.
        created_at (sqlalchemy DateTime): The datetime at creation.
        updated_at (sqlalchemy DateTime): The datetime of last update.
    """
    id = Column(String(60), primary_key=True)
    created_at = Column(DateTime, default=datetime.utcnow(), nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow(), nullable=False)

    def __init__(self, *args, **kwargs):
        """Instatiates the object"""
        self.id = self.__class__.__name__ + "." + str(uuid4())
        self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()
        if kwargs:
            self.__dict__.update(kwargs)
    
    def save(self):
        """Saves new object in the DB"""
        models.storage.new(self)
        models.storage.save()
    
    def update(self, obj_dict=None):
        """Updates and saves object changes in the DB"""
        self.updated_at = datetime.utcnow()
        if obj_dict:
            for k, v in obj_dict.items():
                setattr(self, k, v)
        models.storage.new(self)
        models.storage.save()

    def __repr__(self):
        """Returns a string representation of the objects"""
        return "<{}> <{}>".format(self.__class__.__name__, self.id)