from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from models.basemodel import BaseModel, Base
from models.tenants import Tenant

class Apartment(BaseModel, Base):

    __tablename__ = "apartments"

    apartment_no = Column(String(8), nullable=False)
    room_type = Column(String(16), nullable=False)
    rent = Column(Integer, nullable=False)
    house_id = Column(String(60), ForeignKey("houses.id"), nullable=False)
    tenants = relationship("Tenant", backref="apartments")