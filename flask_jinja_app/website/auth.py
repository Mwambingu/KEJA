#!/usr/bin/env python3
from flask import Blueprint, render_template, request, flash, redirect, url_for
from website.models import Landlord
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        landlord = Landlord.query.filter_by(email=email).first()

        if landlord:
            if check_password_hash(landlord.password, password):
                flash("Logged in successfully!", category='success')
                return redirect(url_for('views.dashboard'))
            else:
                flash("Incorrect password, try again!", category='error')
        else:
            flash("Email does not exist!", category='error')

    return render_template("login.html")


@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        landlord_dict = {}
        email = request.form.get('email')
        first_name = request.form.get('first-name')
        last_name = request.form.get('last-name')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        landlord = Landlord.query.filter_by(email=email).first()

        if landlord:
            flash("Email already exists. Please use the login page.",
                  category='error')

        elif len(email) < 4:
            flash('Email must be greater than 4 characters.', category='error')
            pass

        elif len(first_name) < 2:
            flash('Name must be greater than 2 characters.', category='error')
            pass

        elif len(last_name) < 2:
            flash('Last Name must be greater than 2 characters.', category='error')
            pass

        elif password1 != password2:
            flash('Passwords don\'t match', category='error')
            pass

        elif len(password1) < 7:
            flash('Password is too short! Should be at least 7 characters',
                  category='error')
            pass
        else:
            password = generate_password_hash(password1, method='sha256')

            landlord_dict['first_name'] = first_name
            landlord_dict['last_name'] = last_name
            landlord_dict['email'] = email
            landlord_dict['password'] = password

            print(landlord_dict)

            new_landlord = Landlord(**landlord_dict)
            db.session.add(new_landlord)
            db.session.commit()
            flash('Account successfully created!', category='success')
            return redirect(url_for('views.dashboard'))

    return render_template("signup.html")
