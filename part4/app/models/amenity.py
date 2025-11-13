from .BaseModel import BaseModel
from app.extensions import db
from sqlalchemy.orm import validates, relationship
from .place import place_amenity

class Amenity(BaseModel):
    __tablename__ = 'amenities'

    name = db.Column(db.String(50), nullable=False)
    #places = relationship('Place', secondary=place_amenity, lazy='subquery', backref=db.backref('amenities', lazy=True))

    @validates('name')
    def validate_name(self, key, value):
        if not isinstance(value, str):
            raise ValueError("name must be a string")
        if not value:
            raise ValueError("name can't be empty")
        if len(value) > 50:
            raise ValueError("name must be less than 50 characters")
        return value
