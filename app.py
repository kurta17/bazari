from flask import Flask
from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_login import LoginManager
from views import bp as users_bp

users = {}

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecret'
login_manager = LoginManager()

app.register_blueprint(users_bp)

if __name__ == '__main__':
    app.run(debug=True, port=4900)