# views.py
from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import LoginManager, UserMixin, login_user
from wtforms import StringField, PasswordField, SubmitField
from flask_wtf import FlaskForm
from flask_login import login_manager
from user import User, UserRegistration
import Json

users = {'kurta@gmail.com': {'password': '1234', 'name': 'Kurta'}}

print(users)
bp = Blueprint('users', __name__, template_folder='templates')

login_manager = LoginManager()


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

@bp.route('/groups', methods=['GET', 'POST'])
#@require_login
def groups():
    return render_template('groups.html')


@bp.route('/add_group', methods=['GET', 'POST'])
#@require_login
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
            flash('Registration successful!', 'success')
            return redirect(url_for('users.login'))
    else:
        flash(f'Invalid input! {form.errors}', 'danger')

    return render_template('register.html',form=form)