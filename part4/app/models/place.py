from .BaseModel import BaseModel
from app.extensions import db
from sqlalchemy.orm import validates, relationship


place_amenity = db.Table('place_amenity',
    db.Column('place_id', db.String(36), db.ForeignKey('places.id'), primary_key=True),
    db.Column('amenity_id', db.String(36), db.ForeignKey('amenities.id'), primary_key=True)
)

class Place(BaseModel):
    __tablename__ = 'places'

    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(5000))
    price = db.Column(db.Float, nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    owner_id = db.Column(db.String(60), db.ForeignKey('users.id') , nullable=False)
    reviews = relationship('Review', backref='place', lazy=True)
    amenities = relationship('Amenity', secondary=place_amenity, lazy='subquery', backref=db.backref('places', lazy=True))

    @validates("title")
    def validate_title(self, key, value):
        if not isinstance(value, str):
            raise TypeError("Title must be a string")
        if not value:
            raise ValueError("Title can't be empty")
        if len(value) > 100:
            raise ValueError("Title must be less than 100 charaters")
        return value


    @validates("price")
    def validate_price(self, key, value):
        if not isinstance(value, (int, float)):
            raise TypeError("Price must be an integer")
        if value < 0:
            raise ValueError("Price must be positive")
        return value


    @validates("description")
    def validate_description(self, key, value):
        if not isinstance(value, str):
            raise TypeError("Description must be a string")
        return value

    @validates("latitude")
    def validate_latitude(self, key, value):
        if not isinstance(value, (int, float)):
            raise TypeError("Latitude must be a float")
        if value < -90 or value > 90:
            raise ValueError("Latitude must be in range of -90.0 to 90.0")
        return value


    @validates("longitude")
    def validate_longitude(self, key, value):
        if not isinstance(value, (int, float)):
            raise TypeError("Longitude must be a float")
        if value < -180 or value > 180:
            raise ValueError("Longitude must be in range of -180.0 to 180.0")
        return value


    def add_review(self, review):
        """Add a review to the place."""
        self.reviews.append(review)

    def add_amenity(self, amenity):
        """Add an amenity to the place."""
        self.amenities.append(amenity)
