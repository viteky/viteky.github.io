from credits import db, login_manager
from flask_login import UserMixin
from datetime import datetime

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    first_name = db.Column(db.String(20), nullable=False)
    last_name = db.Column(db.String(20), nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default="default_user.jpg")
    password = db.Column(db.String(60), nullable=False)
    claims = db.relationship('Claim', backref='user', lazy=True)
    roles = db.relationship('Role', backref='user', lazy=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.first_name}', '{self.last_name}', '{self.image_file}')"


class Role(db.Model):
    role = db.Column(db.String(20), primary_key=True, default='viewer')
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)


class Claim(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.String(10), nullable=False)
    invoice_num = db.Column(db.String(10), nullable=False, unique=True)
    invoice_date = db.Column(db.DateTime, nullable=False)
    run_num = db.Column(db.String(5), nullable=False)
    notify_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    driver = db.Column(db.String(20), default='Unknown')
    picker = db.Column(db.String(20), default='Unknown')
    notes = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    items = db.relationship('Item', backref='claim_id', lazy=True)


class Item(db.Model):
    id = db.Column(db.Integer, db.ForeignKey('claim.id'), nullable=False)
    item_num = db.Column(db.String(6), nullable=False, primary_key=True)
    units = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float)
    status = db.Column(db.String(20), nullable=False, default='Pending')
    reason_code = db.Column(db.String(1))

