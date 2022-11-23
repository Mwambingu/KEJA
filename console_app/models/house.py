from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from models.basemodel import BaseModel, Base
from models.apartment import Apartment

class House(BaseModel, Base):
    __tablename__ = "houses"
    house_name = Column(String(32), nullable=False)
    landlord_id = Column(String(60), ForeignKey("landlords.id"), nullable=False)
    number_of_apartments = Column(Integer, default=0, nullable=True)
    apartments = relationship("Apartment", backref="houses", cascade="all, delete")