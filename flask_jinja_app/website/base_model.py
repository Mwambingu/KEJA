import datetime
from uuid import uuid4
from . import db


class BaseModel:
    id = db.Column(db.String(64), primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    def __init__(self, *args, **kwargs):
        self.id = self.__class__.__name__ + str(uuid4())
        self.created_at = datetime.datetime.utcnow()
        self.updated_at = datetime.datetime.utcnow()

        if kwargs:
            self.__dict__.update(kwargs)

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update_obj(self, obj_dict):
        if obj_dict:
            self.updated_at = datetime.datetime.utcnow()
            self.__dict__.update(obj_dict)
            db.session.merge(self)
            db.session.commit()

    def __repr__(self):
        return "<{}> <{}>: {}".format(self.__class__.__name__, self.id, self.__dict__)
