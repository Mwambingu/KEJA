#!/usr/bin/env python3
from . import db
from .base_model import BaseModel
from flask_login import UserMixin


class Landlord(BaseModel, db.Model, UserMixin):
    """The landlord db model"""
    __tablename__ = "landlords"
    first_name = db.Column(db.String(16), nullable=False)
    last_name = db.Column(db.String(16), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(512), nullable=False)
    tenants = db.relationship(
        "Tenant", backref="landlords", cascade="all, delete", lazy=True,)
    houses = db.relationship("House", backref="landlords",
                             cascade="all, delete", lazy=True)


class House(BaseModel, db.Model):
    """The house db model"""
    __tablename__ = "houses"
    house_name = db.Column(db.String(32), nullable=False)
    landlord_id = db.Column(db.String(64), db.ForeignKey(
        'landlords.id'), nullable=False)
    apartments = db.relationship(
        "Apartment", backref="houses", cascade="all, delete", lazy=True)

    def house_tenants(self):
        """Returns the number of tenants in the house"""
        rented_apartments = []
        apartments = self.apartments

        for apartment in apartments:
            if apartment.apt_tenant:
                rented_apartments.append(apartment)

        if rented_apartments:
            return len(rented_apartments)

        return 0


class Apartment(BaseModel, db.Model):
    """The apartment db model"""
    __tablename__ = "apartments"
    apt_no = db.Column(db.String(32), nullable=False)
    room_type = db.Column(db.String(32), nullable=False)
    rent = db.Column(db.Integer, nullable=False)
    house_id = db.Column(db.String(64), db.ForeignKey(
        "houses.id"), nullable=False)
    apt_tenant = db.relationship(
        "Tenant", backref="apartments", lazy=True)


class Tenant(BaseModel, db.Model, UserMixin):
    """The tenant db model"""
    __tablename__ = "tenants"
    first_name = db.Column(db.String(16), nullable=False)
    last_name = db.Column(db.String(16), nullable=False)
    tenant_id = db.Column(db.String(64), unique=True, nullable=False)
    password = db.Column(db.String(512), nullable=False)
    apt_id = db.Column(db.String(64), db.ForeignKey(
        "apartments.id"), nullable=True)
    landlord_id = db.Column(db.String(64), db.ForeignKey(
        "landlords.id"), nullable=False)


class Payments(BaseModel, db.Model):
    "Payment db Model"
    pass
