from flask import Flask, Blueprint
from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_login import LoginManager


bp = Blueprint('users',__name__,template_folder='templates')

@bp.route('/login')
def login():
    return render_template('login.html')


@bp.route('/register')
def register():
    return render_template('register.html')