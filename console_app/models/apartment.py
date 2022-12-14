"""
Contains the Apartment class
"""
from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from models.basemodel import BaseModel, Base
from models.tenants import Tenant


class Apartment(BaseModel, Base):
    """Represents an Apartment for MySQL database

    Inherits from SQLAlchemy Base and links to the MySQL table apartments

    Attributes:
    __tablename__ (str): The name of the MySQL table to store Apartments.
    apartment_no (sqlalchemy String): The apartment no.
    room_type (sqlalchemy String): The room type of the apartment.
    rent (sqlalchemy Integer): The rent amount of the apartment.
    house_id (sqlalchemy String): The house_id of the apartment.
    tenants (sqlalchemy relationship): tenant-apartment relationship
    """

    __tablename__ = "apartments"

    apartment_no = Column(String(8), nullable=False)
    room_type = Column(String(16), nullable=False)
    rent = Column(Integer, nullable=False)
    house_id = Column(String(60), ForeignKey("houses.id"), nullable=False)
    tenants = relationship("Tenant", backref="apartments")
