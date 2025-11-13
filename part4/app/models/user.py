from .BaseModel import BaseModel
from app.extensions import bcrypt, db
import re
from sqlalchemy.orm import validates, relationship


regex = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')


class User(BaseModel):
    __tablename__ = 'users'

    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(128), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    places = relationship('Place', backref='user', lazy=True)
    reviews= relationship('Review', backref='user', lazy=True)


    @validates('first_name')
    def validate_first_name(self, key, value):
        if not value:
            raise ValueError("Firstname can't be empty")
        if len(value) > 50:
            raise ValueError("Firstname must be less than 50 characters")
        if not isinstance(value, str):
            raise TypeError("Firstname must be a string")        
        return value

    @validates('last_name')
    def validate_last_name(self, key, value):
        if not value:
            raise ValueError("Lastname can't be empty")
        if len(value) > 50:
            raise ValueError("Lastname must be less than 50 characters")
        if not isinstance(value, str):
            raise TypeError("Lastname must be a string")
        return value

    @validates('email')
    def validate_email(self, key, value):
        if not re.fullmatch(regex, value):
            raise ValueError("Email not valid format")
        if not isinstance(value, str):
            raise TypeError("Email must be a string")
        if not value:
            raise ValueError("Email can't be empty")        
        return value

    def hash_password(self, password):
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

    def verify_password(self, password):
        return bcrypt.check_password_hash(self.password, password)
