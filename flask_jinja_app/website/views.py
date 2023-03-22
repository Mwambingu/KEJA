#!/usr/bin/env python3
from flask import Blueprint, render_template, request, flash, redirect, url_for

from flask_login import login_required, current_user
from .models import Landlord, House, Tenant, Apartment
from . import db

views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
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

        return redirect(url_for('views.index'))
    return render_template("dashboard.html", landlord=current_user)


# @views.route('/dashboard')
# @login_required
# def dashboard():
#     return render_template("dashboard.html",  landlord=current_user)


@views.route('/houses')
@login_required
def house():
    return render_template("houses.html", landlord=current_user)


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
