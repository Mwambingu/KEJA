from basemodel import BaseModel
from sqlalchemy import Column, String

class(BaseModel):
    first_name = Column(String(16), nullable=False)
    last_name = Column(String(16), nullable=False)
    email = Column(String(32), nullable=False)
    password = Column(String(32), nullable=False)

