from .BaseModel import BaseModel
from app.extensions import db
from sqlalchemy.orm import validates

class Review(BaseModel):
    __tablename__ = 'reviews'

    text = db.Column(db.String(5000), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    place_id = db.Column(db.String(60), db.ForeignKey('places.id'), nullable=False)
    user_id = db.Column(db.String(60), db.ForeignKey('users.id'), nullable=False)


    @validates
    def validates_text(self, key, value):
        if not isinstance(value, str):
            raise TypeError("Text must be a string")
        if not value:
            raise ValueError("Text can't be empty string")
        return value


    @validates
    def validates_rating(self, key, value):
        if not isinstance(value, int):
            raise TypeError("Rating must be an integer")
        if value < 1 or value > 5:
            raise ValueError("Rating must be from 1 to 5")
        return value
        