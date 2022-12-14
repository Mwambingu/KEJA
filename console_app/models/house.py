"""
Contains the House class
"""
from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from models.basemodel import BaseModel, Base
from models.apartment import Apartment


class House(BaseModel, Base):
    """Represents an House for MySQL database

    Inherits from SQLAlchemy Base and links to the MySQL table houses

    Attributes:
    __tablename__ (str): The name of the MySQL table to store houses.
    house_name (sqlalchemy String): The house name.
    landlord_id (sqlalchemy String): The landlord id of the house.
    number_of_apartments (sqlalchemy Integer): The number of apartments under the house.
    apartments (sqlalchemy relationship): apartment-house relationship
    """
    __tablename__ = "houses"
    house_name = Column(String(32), nullable=False)
    landlord_id = Column(
        String(60),
        ForeignKey("landlords.id"),
        nullable=False)
    number_of_apartments = Column(Integer, default=0, nullable=True)
    apartments = relationship(
        "Apartment",
        backref="houses",
        cascade="all, delete")
