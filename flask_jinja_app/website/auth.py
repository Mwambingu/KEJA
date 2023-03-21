#!/usr/bin/env python3
from flask import Blueprint, render_template, request, flash

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    data = request.form
    print(data)
    return render_template("login.html")


@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('first-name')
        last_name = request.form.get('last-name')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        if len(email) < 4:
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
            flash('Account successfully created!', category='success')

    return render_template("signup.html")
