#!/usr/bin/env python3
from flask import Blueprint, render_template

views = Blueprint('views', __name__)

@views.route('/')
def index():
    return render_template("dashboard.html")

@views.route('/dashboard')
def dashboard():
    return render_template("dashboard.html")

@views.route('/houses')
def house():
    return render_template("houses.html")

@views.route('/messages')
def message():
    return render_template("messages.html")

@views.route('/payments')
def payment():
    return render_template("payments.html")

@views.route('/tenants')
def tenant():
    return render_template("tenants.html")