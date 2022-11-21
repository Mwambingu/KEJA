from sqlalchemy import Column, String, Integer, ForeignKey
from models.basemodel import BaseModel, Base

class Apartment(BaseModel, Base):

    __tablename__ = "apartments"

    apartment_no = Column(String(8), nullable=False)
    room_type = Column(String(16), nullable=False)
    rent = Column(Integer, nullable=False)
    house_id = Column(String(32), nullable=True)
