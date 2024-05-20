from flask_login import UserMixin


class User(UserMixin):
    def __init__(self, email, user_dict):
        self.id = email
        self.password = user_dict['password']
        self.name = user_dict['name']

        super().__init__()
