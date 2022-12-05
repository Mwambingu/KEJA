from models.basemodel import BaseModel, Base
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from models.house import House
from models.tenants import Tenant

class Landlord(BaseModel, Base):
    __tablename__ = "landlords"
    
    first_name = Column(String(16), nullable=False)
    last_name = Column(String(16), nullable=False)
    email = Column(String(32), nullable=False)
    password = Column(String(32), nullable=False)
    houses = relationship("House", backref="landlords", cascade="all, delete")
    tenants = relationship("Tenant", backref="landlords", cascade="all, delete")