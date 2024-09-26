import os
from flask import Flask
from flask_login import LoginManager
import redis
from db_utils import get_db_connection

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecret'

redis_client = redis.StrictRedis(
    host=os.getenv('REDIS_HOST', 'redis'), 
    port=int(os.getenv('REDIS_PORT', 6379)),
    db=0
)
login_manager = LoginManager(app)
login_manager.login_view = 'users.login'

from model import load_user

login_manager.user_loader(load_user)

from views import bp as user_bp
app.register_blueprint(user_bp)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000, debug=True)
