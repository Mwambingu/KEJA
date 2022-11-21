#!/usr/bin/env python3
"""
Contains the base for all models.
"""
from datetime import datetime
from sqlalchemy import Column, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from uuid import uuid4
from sqlalchemy.sql import func
import models

Base = declarative_base()

class BaseModel():
    id = Column(String(60), primary_key=True)
    created_at = Column(DateTime, default=datetime.utcnow(), nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow(), nullable=False)

    def __init__(self, *args, **kwargs):
        self.id = self.__class__.__name__ + "." + str(uuid4())
        self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()
        if kwargs:
            self.__dict__.update(kwargs)
    
    def save(self):

        models.storage.new(self)
        models.storage.save(self)
    
    def __repr__(self):
        return "<{}> <{}>".format(self.__class__.__name__, self.id)