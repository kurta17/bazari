# views.py
from flask import Blueprint, render_template

users = {'kere':{'password': '12345',"email": '123'}}
bp = Blueprint('users', __name__, template_folder='templates')

@bp.route('/')
def home():
    return render_template('home.html')


@bp.route('/login', methods=['GET', 'POST'])
def login():
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
    if request.method == 'POST':
        print(request.form)
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        if password != confirm_password:
            flash('Passwords do not match!', 'danger')
        else:
            
            flash('Registration successful!', 'success')
            return redirect(url_for('users.login'))

    return render_template('register.html')