from flask_restx import Namespace, Resource, fields
from app.services import facade
from app.extensions import db
from flask_jwt_extended import jwt_required, get_jwt


api = Namespace('amenities', description='Amenity operations')

# Define the amenity model for input validation and documentation
amenity_model = api.model('Amenity', {
    'name': fields.String(required=True, description='Name of the amenity')
})

@api.route('/')
class AmenityList(Resource):
    @api.expect(amenity_model)
    @api.response(201, 'Amenity successfully created')
    @api.response(400, 'Invalid input data')
    @jwt_required()
    def post(self):
        """Register a new amenity"""
        current_user = get_jwt()
        if not current_user.get("is_admin"):
            return {'error': 'Admin privileges required'}, 403
        
        amenity_data = api.payload

        all_amenities = facade.get_all_amenities()

        for existing_name in all_amenities:
                if (existing_name.name == amenity_data.get('name')):
                    return {"error": "Amenity already exist"}
        try:
            new_amenity = facade.create_amenity(amenity_data)
        except:
            return {"error": "Invalid input data"}, 400
        return {'id': new_amenity.id, 'name': new_amenity.name}, 201
    

    @api.response(200, 'List of amenities retrieved successfully')
    def get(self):
        """Retrieve a list of all amenities"""
        all_amenities = facade.get_all_amenities()
        return [
            {
                'id': all_amenities_items.id,
                'name': all_amenities_items.name
            }
            for all_amenities_items in all_amenities
        ], 200

@api.route('/<amenity_id>')
class AmenityResource(Resource):
    @api.response(200, 'Amenity details retrieved successfully')
    @api.response(404, 'Amenity not found')
    def get(self, amenity_id):
        """Get amenity details by ID"""
        amenity = facade.get_amenity(amenity_id)
        if not amenity:
            return {'error': 'Amenity not found'}, 404
        return {'id': amenity.id, 'name': amenity.name}


    @api.expect(amenity_model)
    @api.response(200, 'Amenity updated successfully')
    @api.response(404, 'Amenity not found')
    @api.response(400, 'Invalid input data')
    @jwt_required()
    def put(self, amenity_id):
        """Update an amenity's information"""
        #first on retrouve l'amenity'
        current_user = get_jwt()
        if not current_user.get('is_admin'):
            return {'error': 'Admin privileges required'}, 403
        
        amenity_inDB = facade.get_amenity(amenity_id)
        if not amenity_inDB:
            return {'error': "Amenity not found"}, 404
        # on update ce qu'il faut update
            #on charge le user present dans la DB
        updated_amenity = api.payload
            #on update les champs
        for key, value in updated_amenity.items():
            if not hasattr(amenity_inDB, key):
                return {"error": "Invalid input data"}, 400
        try:
            facade.update_amenity(amenity_inDB.id, updated_amenity)
        except:
            return {"error": "Invalid input data"}, 400
        return {'message': 'Amenity updated successfully'}, 200
