import datetime
from uuid import uuid4
from . import db

class BaseModel():
    id = db.Column(db.String(64), primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    def __init__(self, *args, **kwargs):
        self.id = __class__.__name__ + str(uuid4())
