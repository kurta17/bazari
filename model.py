from flask_login import UserMixin
from wtforms import PasswordField, StringField, SubmitField
from wtforms.validators import DataRequired, Email
from flask_wtf import FlaskForm
from db_utils import get_db_connection

class User(UserMixin):
    def __init__(self, id, gmail, password, name):
        self.id = id
        self.gmail = gmail
        self.password = password
        self.name = name


class UserRegistration(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired()])
    submit = SubmitField('Register')

def load_user(user_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE id = %s", (user_id,))
    user = cur.fetchone()
    cur.close()
    conn.close()

    if user:
        return User(id=user[0], gmail=user[1], password=user[2], name=user[3])
    return None