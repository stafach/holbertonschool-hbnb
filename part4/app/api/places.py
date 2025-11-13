from flask_restx import Namespace, Resource, fields
from app.services import facade
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from app.extensions import db

api = Namespace('places', description='Place operations')

# Define the models for related entities
amenity_model = api.model('PlaceAmenity', {
    'id': fields.String(description='Amenity ID'),
    'name': fields.String(description='Name of the amenity')
})

user_model = api.model('PlaceUser', {
    'id': fields.String(description='User ID'),
    'first_name': fields.String(description='First name of the owner'),
    'last_name': fields.String(description='Last name of the owner'),
    'email': fields.String(description='Email of the owner')
})

# Define the place model for input validation and documentation
place_model = api.model('Place', {
    'title': fields.String(required=True, description='Title of the place'),
    'description': fields.String(description='Description of the place'),
    'price': fields.Float(required=True, description='Price per night'),
    'latitude': fields.Float(required=True, description='Latitude of the place'),
    'longitude': fields.Float(required=True, description='Longitude of the place'),
    'owner_id': fields.String(required=True, description='ID of the owner')
    #'amenities': fields.List(fields.String, required=True, description="List of amenities ID's")
})


@api.route('/')
class PlaceList(Resource):
    @api.expect(place_model)
    @api.response(201, 'Place successfully created')
    @api.response(400, 'Invalid input data')
    @api.response(404, 'User not found')
    @jwt_required()
    def post(self):
        """Register a new place"""
        current_user = get_jwt_identity()
        place_data = api.payload
        place_owner = facade.get_user(place_data.get('owner_id'))
        if not place_owner:
            return {"error": "User not found"}, 404
        try:
            new_place = facade.create_place(place_data)
        except:
            return {"error": "Invalid input data"}, 400
        
        return {
            "id": new_place.id,
            'title': new_place.title,
            'description': new_place.description,
            'price': new_place.price,
            'latitude': new_place.latitude,
            'longitude': new_place.longitude,
            'owner_id': new_place.owner_id,
        }, 201

    @api.response(200, 'List of places retrieved successfully')
    def get(self):
        """Retrieve a list of all places"""
        all_places = facade.get_all_places()
        return [
            {
                "id": all_places_items.id,
                "title": all_places_items.title,
                "latitude": all_places_items.latitude,
                "longitude": all_places_items.longitude
            }
            for all_places_items in all_places
        ], 200

@api.route('/<place_id>')
class PlaceResource(Resource):
    @api.response(200, 'Place details retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """Get place details by ID"""
        place = facade.get_place(place_id)
        if not place:
            return {'error': 'Place not found'}, 404

        amenities = place.amenities
        owner = facade.get_user(place.owner_id)

        return {
            "id": place.id,
            "title": place.title,
            "description": place.description,
            "latitude": place.latitude,
            "longitude": place.longitude,
            "owner": {
                "id": owner.id,
                "first_name": owner.first_name,
                "last_name": owner.last_name,
                "email": owner.email
            },
            "amenities": [
                {"id": a.id, "name": a.name} for a in amenities
            ]
        }, 200

    @api.expect(place_model, validate=True)
    @api.response(200, 'Place updated successfully')
    @api.response(404, 'Place not found')
    @api.response(400, 'Invalid input data')
    @jwt_required()
    def put(self, place_id):
        """Update a place's information"""
        place_inDB = facade.get_place(place_id)
        if not place_inDB:
            return {'error': "Place not found"}, 404

        # Récupère id du user connecté
        current_user = get_jwt_identity()
        # Verif status du user (admin or not)
        claims = get_jwt()
        is_admin = claims.get('is_admin', False)

        # Vérifie que l'user actuel est l'owner ou un admin
        if not is_admin and place_inDB.owner_id != current_user:
            return {'error': 'Unauthorized action'}, 403
        
        data = api.payload
        for key, value in data.items():
            if not hasattr(place_inDB, key):
                return {"error": "Invalid input data"}, 400
        try:
            facade.update_user(place_inDB.id, data)
        except:
            return {"error": "Invalid input data"}, 400
        return {'message': "Place updated successfully"}, 200

@api.route('/<place_id>/reviews')
class PlaceReviewList(Resource):
    @api.response(200, 'List of reviews for the place retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """Get all reviews for a specific place"""
        existing_place = facade.get_place(place_id)
        if not existing_place:
            return {"error": "Place not found"}, 404
        return [
            {
                "id": existing_place_items.id,
                "text": existing_place_items.text,
                "rating": existing_place_items.rating
            }
            for existing_place_items in existing_place.reviews
        ], 200