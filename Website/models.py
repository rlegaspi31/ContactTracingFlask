from datetime import datetime
from Website import db




class User(db.Model):
    id = db.Column(db.Integer, unique=True, primary_key=True, autoincrement=True)
    first = db.Column(db.String(120), unique=False, nullable=False)
    last = db.Column(db.String(120), unique=False, nullable=False)
    age = db.Column(db.Integer, nullable=False)
    address = db.Column(db.String(120), unique=False, nullable=False)
    email = db.Column(db.String(60), unique=True, nullable=False)
    phone = db.Column(db.Integer, unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default="default.jpg")
    time_check = db.Column(db.DateTime, nullable=False, default=datetime.now)
    data = db.relationship("DataRegistered", backref="author", lazy=True)

    def __repr__(self):
        return (
            f"User({self.first}, {self.last}, {self.age}, {self.phone}, {self.address})"
        )


class DataRegistered(db.Model):
    id = db.Column(db.Integer, unique=True, primary_key=True, autoincrement=True)
    date_recorded = db.Column(db.DateTime, nullable=False, default=datetime.now)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    def __repr__(self):
        return f"Data({self.date_recorded})"
