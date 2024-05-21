import json
import os
from flask_login import UserMixin
from wtforms import StringField, PasswordField, SubmitField
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, Email

class User(UserMixin):
    def __init__(self, email, user_dict):
        self.id = email
        self.password = user_dict['password']
        self.name = user_dict['name']

        super().__init__()

class UserRegistration(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired()])
    submit = SubmitField('Register')

initial_users = {'kurta@gmail.com': {'password': '1234', 'name': 'Kurta'}}


def save_users_to_file():
    with open('users.json', 'w') as f:
        json.dump(users, f)


def load_users_from_file():
    try:
        with open('users.json', 'r') as f:
            users = json.load(f)
    except:
        users = initial_users

    return users

