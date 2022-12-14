"""
Contains the Landlord class
"""
from models.basemodel import BaseModel, Base
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from models.house import House
from models.tenants import Tenant


class Landlord(BaseModel, Base):
    """Represents an Landlord for MySQL database

    Inherits from SQLAlchemy Base and links to the MySQL table landlord

    Attributes:
    __tablename__ (str): The name of the MySQL table to store landlords.
    first_name (sqlalchemy String): The first name of the landlord.
    last_name (sqlalchemy String): The last name of the landlord.
    email (sqlalchemy String): The email of the landlord.
    password (sqlalchemy String): The password of the landlord.
    houses (sqlalchemy relationship): house-landlord relationship
    tenants (sqlalchemy relationship): tenant-landlord relationship
    """
    __tablename__ = "landlords"

    first_name = Column(String(16), nullable=False)
    last_name = Column(String(16), nullable=False)
    email = Column(String(32), nullable=False)
    password = Column(String(32), nullable=False)
    houses = relationship("House", backref="landlords", cascade="all, delete")
    tenants = relationship(
        "Tenant",
        backref="landlords",
        cascade="all, delete")
