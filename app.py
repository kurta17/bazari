from flask import Flask
from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_login import LoginManager, UserMixin
from views import bp as users_bp, users
from user import User


app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecret'

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def get_user(id: str) -> User:
    user_dict = users.get(id)
    if user_dict:
        return User(id, user_dict)
    else:
        return None
    
@app.route('/users')    
def print_users():
    print(users)
    return users 


app.register_blueprint(users_bp)

if __name__ == '__main__':
    app.run(debug=True, port=4900)
