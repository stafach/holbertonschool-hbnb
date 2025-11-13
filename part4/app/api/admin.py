from flask import request
from flask_restx import Namespace, Resource
from flask_jwt_extended import jwt_required, get_jwt
from app.services import facade
from app.extensions import db

api = Namespace('admin', description='Admin operations')


############################### Admin: create new user ####################################3
@api.route('/users/')
class AdminUserCreate(Resource):
    @jwt_required()
    def post(self):
        current_user = get_jwt()
        if not current_user.get("is_admin"):
            return {'error': 'Admin privileges required'}, 403

        user_data = api.payload
        email = user_data.get('email')

        # Check if email is already in use
        if facade.get_user_by_email(email):
            return {'error': 'Email already registered'}, 400

        try:
            new_user = facade.create_user(user_data)
        except:
            return {"error": "Invalid input data"}, 400
        return {'id': new_user.id, 'success': 'User successfully created'}, 201


############################ Admin: modify existing user #################################
@api.route('/users/<user_id>')
class AdminUserModify(Resource):
    @jwt_required()
    def put(self, user_id):
        current_user = get_jwt()
        if not current_user.get('is_admin'):
            return {'error': 'Admin privileges required'}, 403

        data = api.payload
        email = data.get('email')

        # Ensure email uniqueness
        if email:
            existing_user = facade.get_user_by_email(email)
            if existing_user and existing_user.id != user_id:
                return {'error': 'Email already in use'}, 400

        user_inDB = facade.get_user(user_id)
        if not user_inDB:
            return "User not found", 404
        for key, value in data.items():
            if not hasattr(user_inDB, key):
                return {"error": "Invalid input data"}, 400
        try:
            user_inDB.first_name = data.get('first_name', user_inDB.first_name)
        except:
            return {"error": "Invalid input data"}, 400
        try:
            user_inDB.last_name = data.get('last_name', user_inDB.last_name)
        except:
            return {"error": "Invalid input data"}, 400
        try:
            user_inDB.email = data.get('email', user_inDB.email)
        except:
            return {"error": "Invalid input data"}, 400
        try:
            new_password = data.get('password')
            if new_password:
                user_inDB.hash_password(new_password)
        except:
            return {"error": "Invalid input data"}, 400
        
        db.session.commit()
        return {'id': user_inDB.id, 'first_name': user_inDB.first_name, 'last_name': user_inDB.last_name, 'email': user_inDB.email, 'pswd': user_inDB.password}, 200
    

################################ Admin: modify amenity ############################################
@api.route('/amenities/<amenity_id>')
class AdminAmenityModify(Resource):
    @jwt_required()
    def put(self, amenity_id):
        current_user = get_jwt()
        if not current_user.get('is_admin'):
            return {'error': 'Admin privileges required'}, 403

        amenity_inDB = facade.get_amenity(amenity_id)
        if not amenity_inDB:
            return {'error': "Amenity not found"}, 404
        
        data = api.payload

        for key, value in data.items():
            if not hasattr(amenity_inDB, key):
                return {"error": "Invalid input data"}, 400
        try:
            amenity_inDB.name = data.get('name', amenity_inDB.name)
        except:
            return {"error": "Invalid input data"}, 400
        return {'message': 'Amenity updated successfully'}, 200
