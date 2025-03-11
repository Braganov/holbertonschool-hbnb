"""
Module gérant l'API des avis.
Implémente les endpoints REST pour la gestion des avis utilisateurs.

Fonctionnalités:
    - Création/modification/suppression d'avis
    - Notation des lieux (1-5 étoiles)
    - Filtrage par lieu/utilisateur
    - Pagination des résultats
"""

from flask_restx import Namespace, Resource, fields
from app.services.ReviewFacade import ReviewFacade

from flask_restx import Namespace, Resource, fields
from app.services import facade

api = Namespace('reviews', description='Review operations')

# Define the review model for input validation and documentation
review_model = api.model('Review', {
    'text': fields.String(
        required=True,
        description='Contenu de l\'avis',
        example="Excellent séjour, très bon accueil"
    ),
    'rating': fields.Integer(
        required=True,
        description='Note sur 5',
        min=1,
        max=5,
        example=4
    ),
    'user_id': fields.String(description='ID de l\'auteur'),
    'place_id': fields.String(description='ID du lieu concerné')
})

@api.route('/')
class ReviewList(Resource):
    @api.expect(review_model)
    @api.response(201, 'Review successfully created')
    @api.response(400, 'Invalid input data')
    def post(self):
        """Register a new review"""
        review_data = api.payload
        text = review_data.get('text')
        if not text or not isinstance(text, str) or text.strip() == "":
            return {'error': 'Text is required and must be a non-empty string'}, 400

        rating = review_data.get('rating')
        if not rating or not isinstance(rating, int) or rating < 1 or rating > 5:
            return {'error': 'Rating must be an integer between 1 and 5'}, 400

        user_id = review_data.get('user_id')
        if not user_id or not isinstance(user_id, str) or user_id.strip() == "":
            return {'error': 'User ID is required and must be a non-empty string'}, 400

        place_id = review_data.get('place_id')
        if not place_id or not isinstance(place_id, str) or place_id.strip() == "":
            return {'error': 'Place ID is required and must be a non-empty string'}, 400

        new_review = facade.create_review(review_data)
        return {'id': new_review.id, 'text': new_review.text, 'rating': new_review.rating,
                'user_id': new_review.user_id, 'place_id': new_review.place_id}, 201



    @api.response(200, 'List of reviews retrieved successfully')
    def get(self):
        """Retrieve a list of all reviews"""
        reviews = facade.get_all_reviews()
        return [{'id': review.id, 'text': review.text, 'rating': review.rating,
                 'user_id': review.user_id, 'place_id': review.place_id} for review in reviews], 200

@api.route('/<review_id>')
class ReviewResource(Resource):
    @api.response(200, 'Review details retrieved successfully')
    @api.response(404, 'Review not found')
    def get(self, review_id):
        """Get review details by ID"""
        review = facade.get_review(review_id)
        if not review:
            return {'error': 'Review not found'}, 404
        return {'id': review.id, 'text': review.text, 'rating': review.rating,
                'user_id': review.user_id, 'place_id': review.place_id}, 200

    @api.expect(review_model)
    @api.response(200, 'Review updated successfully')
    @api.response(404, 'Review not found')
    @api.response(400, 'Invalid input data')
    def put(self, review_id):
        """Update a review's information"""
        review_data = api.payload
        review = facade.update_review(review_id, review_data)
        if not review:
            return {'error': 'Review not found'}, 404
        return {'id': review.id, 'text': review.text, 'rating': review.rating,
                'user_id': review.user_id, 'place_id': review.place_id}, 200

    @api.response(200, 'Review deleted successfully')
    @api.response(404, 'Review not found')
    def delete(self, review_id):
        """Delete a review"""
        facade.delete_review(review_id)
        return {'message': 'Review deleted successfully'}, 200

@api.route('/places/<place_id>/reviews')
class PlaceReviewList(Resource):
    @api.response(200, 'List of reviews for the place retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """Get all reviews for a specific place"""
        place = facade.get_place(place_id)
        if not place:
            return {'error': 'Place not found'}, 404
        reviews = facade.get_place_reviews(place_id)
        return [{'id': review.id, 'text': review.text, 'rating': review.rating,
                 'user_id': review.user_id, 'place_id': review.place_id} for review in reviews], 200
