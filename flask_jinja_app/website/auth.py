#!/usr/bin/env python3
from flask import Blueprint, render_template

auth = Blueprint('auth', __name__)


@auth.route('/auth/login')
def login():
    return "<h1>Hello Login</h1>"


@auth.route('/auth/signup')
def signup():
    return "<h1>Hello Signup</h1>"
