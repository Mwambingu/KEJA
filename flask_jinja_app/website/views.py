#!/usr/bin/env python3
from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify, session

import random
from flask_login import login_required, current_user
from .models import Landlord, House, Tenant, Apartment
from werkzeug.security import generate_password_hash
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


def apt_generator(no_of_apts, room_type_dict, house_id):
    """Generates a list of dicts used to create a given number of apartments"""
    apt_dict_list = []

    for i in range(1, no_of_apts + 1):
        temp_apt_dict = {}
        temp_apt_dict['apt_no'] = "D" + str(i)
        temp_apt_dict['house_id'] = house_id
        index = (i % len(room_type_dict)) - 1
        temp_apt_dict.update(room_type_dict[index])
        apt_dict_list.append(temp_apt_dict)
    return apt_dict_list


@views.route('/', methods=['GET', 'POST'])
@views.route('/dashboard', methods=['GET', 'POST'])
@login_required
def index():
    """Handles the home-dashboard"""
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
            tenant_dict['password'] = generate_password_hash(
                get_pass(), method='sha256')
            tenant_dict['landlord_id'] = current_user.id
            new_tenant = Tenant(**tenant_dict)
            db.session.add(new_tenant)
            db.session.commit()
            flash('Tenant added successfully! Username: {} Password: {}'.format(
                tenant_dict['tenant_id'], tenant_dict['password']), category='success')

        return redirect(url_for('views.index'))
    return render_template("dashboard.html", landlord=current_user)


@views.route('/houses', methods=["GET", "POST"])
@login_required
def house():
    """Handles the houses dashboard"""
    houses = current_user.houses

    if request.method == "POST":
        if 'add_house_button' in request.form:
            house_dict = {}
            house_dict['house_name'] = request.form.get('house_name')
            house_dict['landlord_id'] = current_user.id

            new_house = House(**house_dict)
            db.session.add(new_house)
            db.session.commit()
            flash('House Added Successfully', category="success")
        return redirect(url_for("views.house"))

    return render_template("houses.html", landlord=current_user, houses=houses)


@views.route('/messages')
@login_required
def message():
    return render_template("messages.html", landlord=current_user)


@views.route('/payments')
@login_required
def payment():
    return render_template("payments.html", landlord=current_user)


@views.route('/tenants', methods=['GET', 'POST'])
@login_required
def tenant():
    """Handles the tenant dashboard"""
    tenants = current_user.tenants

    if request.method == "POST":
        if "add_tenant_button" in request.form:
            tenant_dict = {}

            tenant_dict["first_name"] = request.form.get('first_name')
            tenant_dict["last_name"] = request.form.get('last_name')
            tenant_dict["landlord_id"] = current_user.id
            tenant_dict['tenant_id'] = (
                tenant_dict['first_name'][:2] + tenant_dict['last_name'][:2] + str(random_int)).upper()
            tenant_dict['password'] = generate_password_hash(
                get_pass(), method='sha256')

            new_tenant = Tenant(**tenant_dict)

            new_tenant.save()
            return redirect(url_for('views.tenant'))

        if "assign_tenant_btn" in request.form:
            comb_id = request.form.get("selected")

            tenant_id = comb_id.split(".")[0]
            apt_id = comb_id.split(".")[1]

            tenant_obj = Tenant.query.get(tenant_id)

            tenant_obj.apt_id = apt_id

            db.session.merge(tenant_obj)
            db.session.commit()

            flash("Tenant Assigned Successfully!", category="success")
            return redirect(url_for('views.tenant'))

    return render_template(
        "tenants.html",
        landlord=current_user,
        tenants=tenants)


@views.route('/get_id', methods=['POST'])
@login_required
def get_id():
    """ Gets houses id and loads it in a session for access by apartments """
    if request.method == 'POST':
        house = json.loads(request.data)
        house_id = house['houseId']

        session["house_id"] = house_id
        return redirect(url_for('views.apartment'))
    return jsonify({})


@views.route('/houses/apartments', methods=['GET', 'POST'])
@login_required
def apartment():
    """ Handles the apartment dashboard """
    apartments = None
    house_id = session.get("house_id")
    house = House.query.get(house_id)
    if house.apartments:
        apartments = Apartment.query.filter_by(
            house_id=house_id).order_by("apt_no")

    if request.method == 'POST':
        if "add_apartment_button" in request.form:
            apartment_dict = {}
            apartment_dict['apt_no'] = request.form.get('apt_no')
            apartment_dict['rent'] = request.form.get('rent')
            apartment_dict['room_type'] = request.form.get('room_type')
            apartment_dict['house_id'] = house.id

            new_apartment = Apartment(**apartment_dict)
            db.session.add(new_apartment)
            db.session.commit()
            flash('Apartment added successfully!', category='success')
            return redirect(url_for('views.apartment'))

        if "gen_apt_button" in request.form:
            apt_dict_list = []
            room_type_dict = []
            no_of_rooms = 0

            if request.form.get('room_type1') != 'Select Room Type':
                room_type_dict.append({'room_type': request.form.get(
                    'room_type1'), 'rent': request.form.get('apt1_rent')})
            if request.form.get('room_type2') != 'Select Room Type':
                room_type_dict.append({'room_type': request.form.get(
                    'room_type2'), 'rent': request.form.get('apt2_rent')})
            if request.form.get('room_type3') != 'Select Room Type':
                room_type_dict.append({'room_type': request.form.get(
                    'room_type3'), 'rent': request.form.get('apt3_rent')})

            no_of_rooms = int(request.form.get('no_of_apts'))

            apt_dict_list = apt_generator(
                no_of_rooms, room_type_dict, house_id)

            for apt_dict in apt_dict_list:
                new_apartment = Apartment(**apt_dict)
                db.session.add(new_apartment)
            db.session.commit()
            flash('Apartments successfully generated!', category='success')
            return redirect(url_for('views.apartment'))

        if "assign_tenant_btn" in request.form:
            update_dict = {}
            value = request.form.get('tenant')

            tenant_id = value.split(".")[0]
            apt_id = value.split(".")[1]
            update_dict['apt_id'] = apt_id

            tenant = Tenant.query.filter_by(id=tenant_id).first()

            tenant.apt_id = apt_id

            db.session.merge(tenant)
            db.session.commit()
            flash("Tenant assigned successfully!", category='success')
            return redirect(url_for('views.apartment'))

    return render_template(
        "apartments.html",
        landlord=current_user,
        house=house,
        apartments=apartments, )


@views.route('/delete-all-apt', methods=['POST'])
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
    return jsonify({})


@views.route('/delete-apt', methods=['POST'])
@login_required
def delete_apt():
    if request.method == 'POST':
        apt_json = json.loads(request.data)
        apt_id = apt_json['apt_id']

        apt = Apartment.query.filter_by(id=apt_id).first()
        db.session.delete(apt)
        db.session.commit()

        flash("Apartment Deleted successfully!", category='success')

    return jsonify({})


@views.route('/delete-hse', methods=['POST'])
@login_required
def delete_hse():
    if request.method == 'POST':
        house_json = json.loads(request.data)
        house_id = house_json['house_id']

        house = House.query.filter_by(id=house_id).first()
        db.session.delete(house)
        db.session.commit()

        flash("House Deleted successfully!", category='success')

    return jsonify({})


@views.route('/delete-all-hse', methods=['POST'])
@login_required
def delete_all_hse():
    if request.method == 'POST':
        houses = current_user.houses

        for house in houses:
            db.session.delete(house)

        db.session.commit()
        flash("All Houses Deleted successfully!", category='success')

    return jsonify({})


@views.route('/delete-tenant', methods=['POST'])
@login_required
def delete_tenant():
    if request.method == 'POST':
        tenant_json = json.loads(request.data)
        tenant_id = tenant_json['tenant_id']

        tenant = Tenant.query.filter_by(id=tenant_id).first()
        db.session.delete(tenant)
        db.session.commit()

        flash("Tenant Deleted successfully!", category='success')

    return jsonify({})


@views.route('/delete-all-tenant', methods=['POST'])
@login_required
def delete_all_tenant():
    if request.method == 'POST':
        tenants = current_user.tenants

        for tenant in tenants:
            db.session.delete(tenant)

        db.session.commit()
        flash("All Tenants Deleted successfully!", category='success')

    return jsonify({})


@views.route('/remove-tenant', methods=['POST'])
@login_required
def remove_tenant():
    tenant = None
    if request.method == 'POST':
        obj_json = json.loads(request.data)
        if "apt_id" in obj_json.keys():
            apt_id = obj_json['apt_id']
            apartment = Apartment.query.filter_by(id=apt_id).first()
            tenant = apartment.apt_tenant[0]

        if "tenant_id" in obj_json.keys():
            tenant_id = obj_json["tenant_id"]
            tenant = Tenant.query.filter_by(id=tenant_id).first()

    if tenant:
        tenant.apt_id = None

        db.session.merge(tenant)
        db.session.commit()
        flash("Tenant Unassigned Successfully!", category="success")

    return jsonify({})
