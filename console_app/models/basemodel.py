#!/usr/bin/env python3
"""
Contains the base for all models.
"""
from sqlalchemy import Column, String, DateTime
from uuid import uuid4
from sqlalchemy.sql import func

class BaseModel():
    id = Column(String(60), primary_key=True)
    created_at = Column(DateTime(timezone=True), server_default=func.utcnow())
    updated_at = Column(DateTime(timezone=True), onupdate=func.utcnow())

    def __init__(self, **args, **kwargs):
        self.id = self.__class__.__name__. + "." + str(uuid4())
        if kwargs:
            self.__dict__.update(kwargs)

