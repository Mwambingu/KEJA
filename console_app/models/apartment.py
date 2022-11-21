from sqlalchemy import Column, String, Integer, ForeignKey
from models.basemodel import BaseModel

class Apartment(BaseModel):

    __tablename__ = "apartments"

    apartment_no = Column(String(8), nullable=False)
    room_type = Column(String(16), nullable=False)
    rent = Column(Integer, nullable=False)
    house_id = Column(String(32), ForeignKey("houses.id"), nullable=True)
