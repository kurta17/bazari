from flask import Flask
from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_login import LoginManager


app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecret'
login_manager = LoginManager()
#coment
