from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class User(UserMixin):
    def __init__(self, username, password):
        self.username = username
        self.password = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password, password)

    def get_id(self):
        return self.username
    
class Category:
    def __init__(self, name, user_name):
        self.name = name
        self.user_name = user_name

class Project:
    def __init__(self, name, description, user_name, category_oid=None):
        self.name = name
        self.description = description
        self.user_name = user_name
        self.category_oid = category_oid
        self.completed = False

class Task:
    def __init__(self, content, project_oid):
        self.content = content
        self.project_oid = project_oid
        self.completed = False