"""
Instantiates a database storage engine (DBStorage).
"""
from models.engine.db import DBStorage

storage = DBStorage()

storage.reload()