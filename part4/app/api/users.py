from flask_restx import Namespace, Resource, fields
from app.services import facade
from flask import jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from app.extensions import db
api = Namespace('users', description='User operations')

# Define the user model for input validation and documentation
user_model = api.model('User', {
    'first_name': fields.String(required=True, description='First name of the user'),
    'last_name': fields.String(required=True, description='Last name of the user'),
    'email': fields.String(required=True, description='Email of the user'),
    'password': fields.String(required=True, description='Password of the user')
})


###################################### Post new user #######################################
@api.route('/')
class UserList(Resource):
    @api.expect(user_model, validate=True)
    @api.response(201, 'User successfully created')
    @api.response(400, 'Email already registered')
    @api.response(400, 'Invalid input data')
    def post(self):
        """Register a new user"""
        user_data = api.payload

        # Simulate email uniqueness check (to be replaced by real validation with persistence)
        existing_user = facade.get_user_by_email(user_data['email'])

        if existing_user:
            return {'error': 'Email already registered'}, 400

        try:
            new_user = facade.create_user(user_data)
        except:
            return {"error": "Invalid input data"}, 400
        return {'id': new_user.id, 'success': 'User successfully created'}, 201

################################### Get list of all users ####################################
    def get(self):
        """Retrieve a List of Users"""
        all_users = facade.get_all()
        return [
            {
                'id': all_users_items.id,
                'first_name': all_users_items.first_name,
                'last_name': all_users_items.last_name,
                'email': all_users_items.email
            }
            for all_users_items in all_users
        ], 200
    

######################## get usr's details by id ########################
@api.route('/<user_id>')
class UserResource(Resource):
    @api.response(200, 'User details retrieved successfully')
    @api.response(404, 'User not found')
    def get(self, user_id):
        """Get user details by ID"""
        user = facade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404
        return {'id': user.id, 'first_name': user.first_name, 'last_name': user.last_name, 'email': user.email}, 200
    
########################## Update usr's info #############################
    @api.expect(user_model)
    @api.response(200, 'User retrieved successfully')
    @api.response(404, 'User not found')
    @jwt_required()
    def put(self, user_id):
        """Update a user"""
        current_user = get_jwt_identity()
        admin = get_jwt()
        #first on retrouve le user
        user_inDB = facade.get_user(user_id)
        if not user_inDB:
            return "User not found", 404

        if current_user != user_inDB.id and not admin.get("is_admin"):
            return {'error': 'Unauthorized action'}, 403
        # on update ce qu'il faut update
        #on charge le user present dans la DB
        updated_user = api.payload
            #on update les champs
        if not admin.get("is_admin"):
            if 'email' in updated_user or 'password' in updated_user:
                return {"error": "You cannot modify email or password."}, 400
        
        for key, value in updated_user.items():
            if not hasattr(user_inDB, key):
                return {"error": "Invalid input data"}, 400
        try:
            facade.update_user(user_inDB.id, updated_user)
        except:
            return {"error": "Invalid input data"}, 400
        return {'message': 'User updated successfully'}, 200
