#!/usr/bin/env python3
from . import db
from base_model import Base

class Landlord(Base, db.Model):
    __tablename__ = "landlords"
    first_name = db.Column(db.String(16), nullable=False)
    last_name = db.Column(db.String(16), nullable=False)
    email = db.Column(db.String(32), unique=True, nullable=False)
    password = db.Column(db.String(64), nullable=False)

class House(Base, db.Model):
    __tablename__ = "houses"
    house_name = db.Column(db.String(32), nullable=False)
    landlord_id = db.Column(db.String(64), db.ForeignKey('landlords.id'), nullable=False)
    number_of_apartments =  db.Column(db.Integer, default=0, nullable=True)

class Apartment(Base, db.Model):
    __tablename__ = "apartments"
    apartment_no = db.Column(db.String(32), nullable=False)
    room_type = db.Column(db.String(32), nullable=False)
    rent = db.Column(db.Integer, nullable=False)
    house_id = db.Column(db.String(64), db.ForeignKey("houses.id"), nullable=False)

class Tenant(Base, db.Model):
    __tablename__ = "tenants"
    first_name = db.Column(db.String(16), nullable=False)
    last_name = db.Column(db.String(16), nullable=False)
    tenant = db.Column(db.String(64), nullable=False)
    password = db.Column(db.String(64), nullable=False)
    apartment_id = db.Column(db.String(64), db.ForeignKey("apartments.id"), nullable=False)
    landlord_id = db.Column(db.String(64), db.ForeignKey("landlords.id"), nullable=False)