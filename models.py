from datetime import date

from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy

bcrypt = Bcrypt()
db = SQLAlchemy()

def connect_db(app):
    """Connect to database"""
    db.app = app
    db.init_app(app)

class User(db.Model):
    """User in the system"""

    __tablename__ = 'users'

    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True,
    )

    username = db.Column(
        db.Text,
        nullable=False,
        unique=True,
    )

    password = db.Column(
        db.Text,
        nullable=False,
    )

    ingredients = db.relationship(
        "Ingredient", backref="user"
    )

    @classmethod
    def signup(cls, username, password):
        """Sign up user.

        Hashes password and adds user to system.
        """

        hashed_pwd = bcrypt.generate_password_hash(password).decode('UTF-8')

        user = User(
            username=username,
            password=hashed_pwd,
        )

        db.session.add(user)
        return user

    @classmethod
    def authenticate(cls, username, password):
        """Find user with `username` and `password`.

        This is a class method (call it on the class, not an individual user.)
        It searches for a user whose password hash matches this password
        and, if it finds such a user, returns that user object.

        If can't find matching user (or if password is wrong), returns False.
        """

        user = cls.query.filter_by(username=username).first()

        if user:
            is_auth = bcrypt.check_password_hash(user.password, password)
            if is_auth:
                return user

        return False

class Ingredient(db.Model):
    """User ingredients"""

    __tablename__ = 'ingredients'

    id = db.Column(
        db.Integer, 
        primary_key=True, 
        autoincrement=True,
        )

    user_id = db.Column(
        db.ForeignKey('users.id'),
    )

    ingredient = db.Column(
        db.Text,
        nullable=False,
    )

    description = db.Column(
        db.Text,
        nullable=False,
    )

    categories = db.Column(
        db.Text,
        nullable=False,
    )

    quantity = db.Column(
        db.Integer,
        nullable=False,
    )

    image = db.Column(
        db.Text,
    )

    purchase_date = db.Column(
        db.Date,
        nullable = False,
    )

    expiration_date = db.Column(
        db.Date,
        nullable = False,
    )

