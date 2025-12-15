from flask import Blueprint, request, jsonify
from utils.database import get_db, save_db, get_next_id
from utils.auth import auth_required
from datetime import datetime

favorites_bp = Blueprint('favorites', __name__)

@favorites_bp.route('/', methods=['GET'])
@auth_required
def get_favorites():
    """Get user's favorite doctors"""
    try:
        db = get_db()
        favorites = db.get('favorites', [])
        doctors = db.get('doctors', [])
        
        # Filter favorites for current user
        user_favorites = [f for f in favorites if f.get('userId') == request.user['id']]
        
        # Add doctor info to each favorite
        for favorite in user_favorites:
            doctor = next((d for d in doctors if d.get('id') == favorite.get('doctorId')), None)
            if doctor:
                favorite['doctor'] = {
                    'name': doctor.get('name'),
                    'specialty': doctor.get('specialty'),
                    'image': doctor.get('image', f"https://i.pravatar.cc/150?u={doctor.get('id')}")
                }
        
        return jsonify({'favorites': user_favorites})
    except Exception as e:
        print(f'Get favorites error: {e}')
        return jsonify({
            'error': {
                'message': 'Failed to retrieve favorites',
                'status': 500
            }
        }), 500

@favorites_bp.route('/', methods=['POST'])
@auth_required
def add_favorite():
    """Add doctor to favorites"""
    try:
        data = request.get_json()
        doctor_id = data.get('doctorId')
        
        if not doctor_id:
            return jsonify({
                'error': {
                    'message': 'Doctor ID is required',
                    'status': 400
                }
            }), 400
        
        db = get_db()
        favorites = db.get('favorites', [])
        
        # Check if already in favorites
        existing = next((f for f in favorites 
                        if f.get('userId') == request.user['id'] 
                        and f.get('doctorId') == doctor_id), None)
        
        if existing:
            return jsonify({
                'error': {
                    'message': 'Doctor already in favorites',
                    'status': 400
                }
            }), 400
        
        # Create new favorite
        new_favorite = {
            'id': get_next_id(favorites),
            'userId': request.user['id'],
            'doctorId': doctor_id,
            'createdAt': datetime.now().isoformat()
        }
        
        favorites.append(new_favorite)
        db['favorites'] = favorites
        save_db(db)
        
        return jsonify({'favorite': new_favorite}), 201
    except Exception as e:
        print(f'Add favorite error: {e}')
        return jsonify({
            'error': {
                'message': 'Failed to add favorite',
                'status': 500
            }
        }), 500

@favorites_bp.route('/<int:doctor_id>', methods=['DELETE'])
@auth_required
def remove_favorite(doctor_id):
    """Remove doctor from favorites"""
    try:
        db = get_db()
        favorites = db.get('favorites', [])
        
        # Find and remove favorite
        initial_count = len(favorites)
        favorites = [f for f in favorites 
                    if not (f.get('userId') == request.user['id'] 
                           and f.get('doctorId') == doctor_id)]
        
        if len(favorites) == initial_count:
            return jsonify({
                'error': {
                    'message': 'Favorite not found',
                    'status': 404
                }
            }), 404
        
        db['favorites'] = favorites
        save_db(db)
        
        return jsonify({'message': 'Favorite removed successfully'})
    except Exception as e:
        print(f'Remove favorite error: {e}')
        return jsonify({
            'error': {
                'message': 'Failed to remove favorite',
                'status': 500
            }
        }), 500
