# views.py
from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import LoginManager, UserMixin, login_user, logout_user
from wtforms import StringField, PasswordField, SubmitField
from flask_wtf import FlaskForm
from flask_login import login_manager
from user import User, UserRegistration
import json
from flask_login import login_required


bp = Blueprint('users', __name__, template_folder='templates')

login_manager = LoginManager()

initial_users = {'kurta@gmail.com': {'password': '1234', 'name': 'Kurta'}}


def load_users_from_file():
    try:
        with open('users.json', 'r') as f:
            users = json.load(f)
    except:
        users = initial_users

    return users

users = load_users_from_file()

def save_users_to_file():
    with open('users.json', 'w') as f:
        json.dump(users, f)

@bp.route('/')
def home():
    return render_template('home.html')


@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        if email in users:
            user = User(email, users[email])
            if user.password ==  password:
                login_user(user)
                flash('Logged in successfully!', 'success')
                return redirect(url_for('users.home'))
            else:
                flash('Incorrect password!', 'danger')
        else:
            flash('User does not exist!', 'danger')
    
    return render_template('login.html')


@bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('users.home'))

@bp.route('/groups', methods=['GET', 'POST'])
@login_required
def groups():
    return render_template('groups.html')


@bp.route('/add_group', methods=['GET', 'POST'])
@login_required
def add_group():
    return render_template('add_group.html')

@bp.route('/register', methods=['GET', 'POST'])
def register():
    form = UserRegistration()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        confirm_password = form.confirm_password.data
        username = form.username.data

        if password != confirm_password:
            flash('Passwords do not match!', 'danger')
        else:
            users[email] = {'password': password, 'name': username}
            save_users_to_file()
            flash('Registration successful!', 'success')
            return redirect(url_for('users.home'))
    else:
        flash(f'Invalid input! {form.errors}', 'danger')

    return render_template('register.html', form=form)