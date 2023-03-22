#!/usr/bin/env python3
from flask import Blueprint, render_template

from flask_login import login_required, current_user

views = Blueprint('views', __name__)


@views.route('/')
@login_required
def index():
    return render_template("dashboard.html")


@views.route('/dashboard')
@login_required
def dashboard():
    return render_template("dashboard.html")


@views.route('/houses')
@login_required
def house():
    return render_template("houses.html")


@views.route('/messages')
@login_required
def message():
    return render_template("messages.html")


@views.route('/payments')
@login_required
def payment():
    return render_template("payments.html")


@views.route('/tenants')
@login_required
def tenant():
    return render_template("tenants.html")
