from werkzeug.security import generate_password_hash, check_password_hash
from . import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    
    # Define a one-to-many relationship with UserHistory
    history = db.relationship('UserHistory', backref='user', lazy=True)

    def __repr__(self):
        return f'<User {self.email}>'

    # Set the password by hashing it
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    # Check the password against the stored hash
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

# New UserHistory model to track user actions
class UserHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    action = db.Column(db.String(255), nullable=False)
    image_path = db.Column(db.String(300), nullable=True)
    timestamp = db.Column(db.DateTime, default=db.func.current_timestamp(), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f'<UserHistory {self.action}>'

