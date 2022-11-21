from sqlalchemy import Column, String, Integer, ForeignKey
from models.basemodel import BaseModel

class House(BaseModel):
    __tablename__ = "houses"
    house_name = Column(String(32), nullable=False)
    landlord_id = Column(String(32), ForeignKey("landlords.id"), nullable=True)
    number_of_apartments = Column(Integer, default=0, nullable=True)

