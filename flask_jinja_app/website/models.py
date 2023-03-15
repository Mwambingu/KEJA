#!/usr/bin/env python3
from . import db
from .base_model import BaseModel


class Landlord(BaseModel, db.Model):
    __tablename__ = "landlords"
    first_name = db.Column(db.String(16), nullable=False)
    last_name = db.Column(db.String(16), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(64), nullable=False)
    tenants = db.relationship(
        "Tenant", backref="landlords", cascade="all, delete", lazy=True,)
    houses = db.relationship("House", backref="landlords",
                             cascade="all, delete", lazy=True)


class House(BaseModel, db.Model):
    __tablename__ = "houses"
    house_name = db.Column(db.String(32), nullable=False)
    landlord_id = db.Column(db.String(64), db.ForeignKey(
        'landlords.id'), nullable=False)
    number_of_apartments = db.Column(db.Integer, default=0, nullable=True)
    apartments = db.relationship(
        "Apartment", backref="houses", cascade="all, delete", lazy=True)


class Apartment(BaseModel, db.Model):
    __tablename__ = "apartments"
    apartment_no = db.Column(db.String(32), nullable=False)
    room_type = db.Column(db.String(32), nullable=False)
    rent = db.Column(db.Integer, nullable=False)
    house_id = db.Column(db.String(64), db.ForeignKey(
        "houses.id"), nullable=False)
    apt_tenant = db.relationship(
        "Tenant", backref="apartments", cascade="all, delete", lazy=True)


class Tenant(BaseModel, db.Model):
    __tablename__ = "tenants"
    first_name = db.Column(db.String(16), nullable=False)
    last_name = db.Column(db.String(16), nullable=False)
    tenant_id = db.Column(db.String(64), unique=True, nullable=False)
    password = db.Column(db.String(64), nullable=False)
    apartment_id = db.Column(db.String(64), db.ForeignKey(
        "apartments.id"), nullable=False)
    landlord_id = db.Column(db.String(64), db.ForeignKey(
        "landlords.id"), nullable=False)
