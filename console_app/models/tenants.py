from sqlalchemy import Column, String, Integer, ForeignKey
from models.basemodel import BaseModel, Base

class Tenant(BaseModel, Base):
    __tablename__ = "tenants"

    first_name = Column(String(16), nullable=False)
    last_name = Column(String(16), nullable=False)
    apartment_id = Column(String(60), ForeignKey("apartments.id"), nullable=True)
    landlord_id = Column(String(60), ForeignKey("landlords.id"), nullable=False)