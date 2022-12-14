"""
Contains the Tenant class
"""
from sqlalchemy import Column, String, Integer, ForeignKey
from models.basemodel import BaseModel, Base

class Tenant(BaseModel, Base):
    """Represents an Tenant for MySQL database

    Inherits from SQLAlchemy Base and links to the MySQL table tenant
    
    Attributes:
    __tablename__ (str): The name of the MySQL table to store tenant.
    first_name (sqlalchemy String): The first name of the tenant.
    last_name (sqlalchemy String): The last name of the tenant.
    password (sqlalchemy String): The password of the tenant.
    apartment_id (sqlalchemy String): The apartment_id of the tenant.
    landlord_id (sqlalchemy String): The landlord_id of the tenant.
    """
    __tablename__ = "tenants"

    first_name = Column(String(16), nullable=False)
    last_name = Column(String(16), nullable=False)
    tenant_id = Column(String(16), nullable=True)
    password = Column(String(32), nullable=True)
    apartment_id = Column(String(60), ForeignKey("apartments.id"), nullable=True)
    landlord_id = Column(String(60), ForeignKey("landlords.id"), nullable=False)