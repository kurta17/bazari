# views.py
from flask import Blueprint, render_template

bp = Blueprint('users', __name__, template_folder='templates')

@bp.route('/login')
def login():
    return render_template('login.html')


@bp.route('/register')
def register():
    return render_template('register.html')