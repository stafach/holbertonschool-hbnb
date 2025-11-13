from flask import Flask

import config

from app.extensions import bcrypt, jwt, db

from flask_restx import Api
from app.api.users import api as users_ns
from app.api.amenities import api as amenities_ns
from app.api.places import api as places_ns
from app.api.reviews import api as review_ns
from app.api.auth import api as auth_ns
from app.api.admin import api as admin_ns

def create_app(config_class=config.DevelopmentConfig):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    bcrypt.init_app(app)

    jwt.init_app(app)

    db.init_app(app)
    
    api = Api(app, version='1.0', title='HBnB API', description='HBnB Application API', doc='/api/v1/')
    api.add_namespace(users_ns, path='/api/v1/users')
    api.add_namespace(amenities_ns, path='/api/v1/amenities')
    api.add_namespace(places_ns, path='/api/v1/places')
    api.add_namespace(review_ns, path='/api/v1/reviews')
    api.add_namespace(auth_ns, path='/api/v1/auth')
    api.add_namespace(admin_ns, path='/api/v1/admin')

    return app
