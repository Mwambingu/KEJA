from sqlalchemy import Column, String, Integer, ForeignKey
from models.basemodel import BaseModel

class Tenant(BaseModel):
    __tablename__ = "tenants"

    first_name = Column(String(16), nullable=False)
    last_name = Column(String(16), nullable=False)
    apartment_id = Column(String(32), ForeignKey("apartments.id"), nullable=True)
