from basemodel import BaseModel
from sqlalchemy import Column, String

class(BaseModel):
    __tablename__ = "landlords"
    
    first_name = Column(String(16), nullable=False)
    last_name = Column(String(16), nullable=False)
    email = Column(String(32), nullable=False)
    password = Column(String(32), nullable=False)

