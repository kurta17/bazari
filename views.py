from datetime import datetime
from flask import Blueprint, flash, json, logging, redirect, render_template, request, url_for
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from model import User, UserRegistration
from db_utils import get_db_connection
import logging
import redis

redis_client = redis.StrictRedis(host='localhost', port=6379, db=0)

bp = Blueprint('users', __name__, template_folder='templates')

@bp.route('/')
def home():
    return render_template('home.html')

@bp.route('/profile')
@login_required
def profile():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT gmail, name, profile_picture FROM users WHERE id = %s", (current_user.id,))
    user_details = cur.fetchone()

    cur.execute("SELECT name FROM groups WHERE admin_id = %s", (current_user.id,))
    user_chats = cur.fetchall()
    cur.close()
    conn.close()

    return render_template('profile.html', user_details=user_details, user_chats=user_chats)

@bp.route('/update_profile_picture', methods=['POST'])
@login_required
def update_profile_picture():
    profile_picture_url = request.form['profile_picture_url']

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("UPDATE users SET profile_picture = %s WHERE id = %s", (profile_picture_url, current_user.id))
    conn.commit()
    cur.close()
    conn.close()

    flash('Profile picture updated successfully!', 'success')
    return redirect(url_for('users.profile'))


@bp.route('/delete_group/<group_name>', methods=['POST'])
@login_required
def delete_group(group_name):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM groups WHERE name = %s AND admin_id = %s", (group_name, current_user.id))
    conn.commit()
    cur.close()
    conn.close()

    flash(f'Group {group_name} deleted!', 'success')
    return redirect(url_for('users.profile'))



@bp.route('/group/<group_name>/messages', methods=['GET'])
@login_required
def get_group_messages(group_name):
    # Fetch messages from Redis
    redis_key = f"{group_name}_messages"
    raw_messages = redis_client.lrange(redis_key, 0, -1)
    
    messages = []

    # Decode and parse messages from Redis
    for message in raw_messages:
        message_data = json.loads(message.decode('utf-8'))
        messages.append({
            'author': message_data['author'],
            'text': message_data['text'],
            'created': message_data['created']  # Already in string format
        })

    # Sort messages by timestamp
    messages = sorted(messages, key=lambda x: x['created'])

    return json.jsonify(messages)



@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE gmail = %s", (email,))
        user = cur.fetchone()
        cur.close()
        conn.close()

        if user:
            logging.debug(f"Retrieved user: {user}")
            logging.debug(f"Password hash: {user[2]}")  # Assuming password is the third column

        if user and check_password_hash(user[2], password):  # Assuming password is the third column
            user_obj = User(id=user[0], gmail=user[1], password=user[2], name=user[3])
            login_user(user_obj)
            flash('Logged in successfully!', 'success')
            return redirect(url_for('users.home'))
        else:
            flash('Invalid email or password', 'danger')
    
    return render_template('login.html')

@bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('users.home'))

@bp.route('/groups', methods=['GET', 'POST'])
@login_required
def groups():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT  groups.name,users.name as group_name FROM groups join users on groups.admin_id = users.id")
    groups = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('groups.html', groups=groups)

@bp.route('/group/<group_name>')
@login_required
def group_detail(group_name):
    # Fetch group details from PostgreSQL
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM groups WHERE name = %s", (group_name,))
    group = cur.fetchone()
    cur.close()
    conn.close()

    if group is None:
        return redirect(url_for('users.groups'))

    redis_key = f"{group_name}_messages"
    raw_messages = redis_client.lrange(redis_key, 0, -1)
    
    messages = []

    for message in raw_messages:
        message_data = json.loads(message.decode('utf-8'))
        messages.append({
            'author': message_data['author'],
            'text': message_data['text'],
            'created': datetime.strptime(message_data['created'], '%Y-%m-%d %H:%M:%S')
        })

    messages = sorted(messages, key=lambda x: x['created'])

    return render_template('group_detail.html', group=group, messages=messages)


@bp.route('/add_message/<group_name>', methods=['POST'])
@login_required
def add_message(group_name):
    if request.method == 'POST':
        author = current_user.name
        text = request.form['text']
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        message = {
            'author': author,
            'text': text,
            'created': timestamp
        }

        message_key = f"{group_name}_messages"
        redis_client.rpush(message_key, json.dumps(message))

        flash('Message added successfully!', 'success')
        return redirect(url_for('users.group_detail', group_name=group_name))


@bp.route('/add_group', methods=['GET', 'POST'])
@login_required
def add_group():
    if request.method == 'POST':
        group_name = request.form['group_name']
        admin_id = current_user.id

        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM groups WHERE name = %s", (group_name,))
        group = cur.fetchone()

        if group:
            flash('Group already exists!', 'danger')
        else:
            cur.execute("INSERT INTO groups (name, admin_id) VALUES (%s, %s)", (group_name, admin_id))
            conn.commit()
            flash('Group created successfully!', 'success')

        cur.close()
        conn.close()

        return redirect(url_for('users.groups'))

    return render_template('add_group.html')


@bp.route('/register', methods=['GET', 'POST'])
def register():
    form = UserRegistration()
    
    if form.validate_on_submit():
        email = form.email.data
        username = form.username.data
        hashed_password = form.password.data  # Replace with actual password hashing logic
        
        conn = get_db_connection()
        cur = conn.cursor()

        # Check if the email already exists
        cur.execute("SELECT COUNT(*) FROM users WHERE gmail = %s", (email,))
        email_exists = cur.fetchone()[0]

        if email_exists:
            flash('Email already exists. Please choose a different email.', 'danger')
        else:
            # Proceed with user registration
            try:
                cur.execute("INSERT INTO users (gmail, password, name) VALUES (%s, %s, %s)", 
                            (email, hashed_password, username))
                conn.commit()
                flash('Registration successful! You can now log in.', 'success')
                return redirect(url_for('users.login'))  # Redirect to login page
            except Exception as e:
                flash(f'An error occurred: {str(e)}', 'danger')
        
        cur.close()
        conn.close()

    for field, errors in form.errors.items():
        for error in errors:
            flash(f'{field.capitalize()}: {error}', 'danger')

    return render_template('register.html', form=form)