from datetime import datetime

from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from extensions import db


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)

    # Basic account details
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(
        db.String(180),
        unique=True,
        nullable=False,
        index=True
    )
    password_hash = db.Column(db.String(255), nullable=False)

    # Student profile details
    phone = db.Column(db.String(20))
    college = db.Column(db.String(200))
    degree = db.Column(db.String(100))
    branch = db.Column(db.String(150))
    current_year = db.Column(db.String(50))
    cgpa = db.Column(db.String(30))
    graduation_year = db.Column(db.String(10))

    # Platform details
    role = db.Column(
        db.String(20),
        default='student',
        nullable=False
    )

    xp = db.Column(
        db.Integer,
        default=0
    )

    streak = db.Column(
        db.Integer,
        default=0
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    last_active = db.Column(
        db.DateTime
    )

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(
            self.password_hash,
            password
        )