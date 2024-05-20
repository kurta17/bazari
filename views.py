# views.py
from flask import Blueprint, render_template,request
from flask_login import LoginManager, UserMixin, current_user, login_required, login_user, logout_user


users = {'kere':{'password': '12345',"email": '123'}}
bp = Blueprint('users', __name__, template_folder='templates')

@bp.route('/login')
def login():
    return render_template('login.html')


@bp.route('/register')
def register():
    return render_template('register.html')

def check_login(name, password):
    if name in users:
        if password == users[name]['password']:
            return True
    return False


@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        if check_login(email, password):
            user = users[email]['id']
            login_user(user)
            flash('You are now logged in', 'success')
            return redirect(url_for('home'))
        flash('Invalid email or password', 'danger')

    return render_template('login.html')