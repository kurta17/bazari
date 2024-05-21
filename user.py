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



