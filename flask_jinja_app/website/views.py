#!/usr/bin/env python3
from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify, session

import random
from flask_login import login_required, current_user
from .models import Landlord, House, Tenant, Apartment
from . import db
import json

views = Blueprint('views', __name__)
random_int = random.randint(1000, 9999)


def get_pass():
    """Generates a random password of 8 characters in length"""
    letters_alpha = [
        "abcdefghijklmnopqrstuvwxyz",
        "abcdefghijklmnopqrstuvwxyz".upper(),
        "1234567890",
        "!@#$%"]
    choice = ""
    pass_size = []
    rand_size = 0
    pass_str = ""

    for i in range(8):
        pass_size = []
        rand_size = 0
        choice = random.choice(letters_alpha)
        size = len(choice)
        for i in range(size):
            pass_size.append(i)
        rand_size = random.choice(pass_size)
        pass_str += choice[rand_size]
    return pass_str


@views.route('/', methods=['GET', 'POST'])
@views.route('/dashboard', methods=['GET', 'POST'])
@login_required
def index():
    if request.method == 'POST':

        if "add_house_button" in request.form:
            house_dict = {}
            house_dict['house_name'] = request.form.get('house_name')
            house_dict['landlord_id'] = current_user.id
            new_house = House(**house_dict)
            db.session.add(new_house)
            db.session.commit()
            flash('House added successfully.', category='success')

        if "add_tenant_button" in request.form:
            tenant_dict = {}
            tenant_dict['first_name'] = request.form.get('first_name')
            tenant_dict['last_name'] = request.form.get('last_name')
            tenant_dict['tenant_id'] = (
                tenant_dict['first_name'][:2] + tenant_dict['last_name'][:2] + str(random_int)).upper()
            tenant_dict['password'] = get_pass()
            tenant_dict['landlord_id'] = current_user.id
            new_tenant = Tenant(**tenant_dict)
            db.session.add(new_tenant)
            db.session.commit()
            flash('Tenant added successfully! Username: {} Password: {}'.format(
                tenant_dict['tenant_id'], tenant_dict['password']), category='success')

        return redirect(url_for('views.index'))
    return render_template("dashboard.html", landlord=current_user)


# @views.route('/dashboard')
# @login_required
# def dashboard():
#     return render_template("dashboard.html",  landlord=current_user)


@views.route('/houses')
@login_required
def house():
    houses = current_user.houses
    print(houses)
    return render_template("houses.html", landlord=current_user, houses=houses)


@views.route('/messages')
@login_required
def message():
    return render_template("messages.html", landlord=current_user)


@views.route('/payments')
@login_required
def payment():
    return render_template("payments.html", landlord=current_user)


@views.route('/tenants')
@login_required
def tenant():
    return render_template("tenants.html", landlord=current_user)


@views.route('/get_id', methods=['POST'])
@login_required
def get_id():
    if request.method == 'POST':
        house = json.loads(request.data)
        house_id = house['houseId']

        session["house_id"] = house_id
        return render_template("apartments.html", landlord=current_user, house_id=house_id)
    return jsonify({})


@views.route('/houses/apartments', methods=['GET', 'POST'])
@login_required
def apartment():
    apartments = None
    house_id = session.get("house_id")
    house = House.query.get(house_id)
    apartments = house.apartments
    print(apartments)

    return render_template("apartments.html", landlord=current_user, house=house, apartments=apartments)


@views.route('/delete', methods=['POST'])
@login_required
def delete_all():
    if request.method == 'POST':
        house_id = session.get("house_id")
        house = House.query.get(house_id)
        apartments = house.apartments

        for apartment in apartments:
            db.session.delete(apartment)
            db.session.commit()

        flash("All apartments Deleted successfully!", category='success')
        return render_template("apartments.html", landlord=current_user, house=house,  house_id=house_id)
    return jsonify({})
