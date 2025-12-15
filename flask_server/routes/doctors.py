from flask import Blueprint, request, jsonify
from utils.database import get_db, save_db, get_next_id
from datetime import datetime

doctors_bp = Blueprint('doctors', __name__)

@doctors_bp.route('/', methods=['GET'])
def get_doctors():
    """Get all doctors"""
    try:
        db = get_db()
        doctors = db.get('doctors', [])
        
        # Add placeholder images if needed
        doctors_with_images = []
        for doctor in doctors:
            doctor_copy = doctor.copy()
            if not doctor_copy.get('image', '').startswith('http'):
                doctor_copy['image'] = f"https://i.pravatar.cc/150?u={doctor_copy.get('id', 0)}"
            doctors_with_images.append(doctor_copy)
        
        return jsonify(doctors_with_images), 200
    except Exception as e:
        print(f'Get doctors error: {e}')
        return jsonify({
            'error': {
                'message': 'Failed to retrieve doctors',
                'status': 500
            }
        }), 500

@doctors_bp.route('/<int:doctor_id>', methods=['GET'])
def get_doctor(doctor_id):
    """Get doctor by ID"""
    try:
        db = get_db()
        doctors = db.get('doctors', [])
        doctor = next((d for d in doctors if d.get('id') == doctor_id), None)
        
        if not doctor:
            return jsonify({
                'error': {
                    'message': 'Doctor not found',
                    'status': 404
                }
            }), 404
        
        # Add placeholder image if needed
        doctor_copy = doctor.copy()
        if not doctor_copy.get('image', '').startswith('http'):
            doctor_copy['image'] = f"https://i.pravatar.cc/150?u={doctor_id}"
        
        return jsonify(doctor_copy), 200
    except Exception as e:
        print(f'Get doctor error: {e}')
        return jsonify({
            'error': {
                'message': 'Failed to retrieve doctor',
                'status': 500
            }
        }), 500

@doctors_bp.route('/', methods=['POST'])
def create_doctor():
    """Create a new doctor"""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['name', 'specialty', 'experience']
        for field in required_fields:
            if field not in data:
                return jsonify({
                    'error': {
                        'message': f'{field} is required',
                        'status': 400
                    }
                }), 400
        
        db = get_db()
        doctors = db.get('doctors', [])
        
        # Create new doctor
        new_doctor = {
            'id': get_next_id(doctors),
            'name': data['name'],
            'specialty': data['specialty'],
            'experience': data['experience'],
            'rating': data.get('rating', 0.0),
            'reviews': data.get('reviews', 0),
            'distance': data.get('distance', '0 km'),
            'available': data.get('available', True),
            'nextAvailable': data.get('nextAvailable', 'Not set'),
            'image': data.get('image', f"https://i.pravatar.cc/150?u={get_next_id(doctors)}"),
            'phone': data.get('phone', ''),
            'email': data.get('email', ''),
            'createdAt': datetime.now().isoformat()
        }
        
        doctors.append(new_doctor)
        db['doctors'] = doctors
        save_db(db)
        
        return jsonify(new_doctor), 201
    except Exception as e:
        print(f'Create doctor error: {e}')
        return jsonify({
            'error': {
                'message': 'Failed to create doctor',
                'status': 500
            }
        }), 500

@doctors_bp.route('/<int:doctor_id>', methods=['PUT'])
def update_doctor(doctor_id):
    """Update doctor by ID"""
    try:
        data = request.get_json()
        
        db = get_db()
        doctors = db.get('doctors', [])
        doctor_index = next((i for i, d in enumerate(doctors) if d.get('id') == doctor_id), None)
        
        if doctor_index is None:
            return jsonify({
                'error': {
                    'message': 'Doctor not found',
                    'status': 404
                }
            }), 404
        
        # Update doctor fields
        doctor = doctors[doctor_index]
        updatable_fields = ['name', 'specialty', 'experience', 'rating', 'reviews', 
                           'distance', 'available', 'nextAvailable', 'image', 'phone', 'email']
        
        for field in updatable_fields:
            if field in data:
                doctor[field] = data[field]
        
        doctor['updatedAt'] = datetime.now().isoformat()
        
        doctors[doctor_index] = doctor
        db['doctors'] = doctors
        save_db(db)
        
        return jsonify(doctor), 200
    except Exception as e:
        print(f'Update doctor error: {e}')
        return jsonify({
            'error': {
                'message': 'Failed to update doctor',
                'status': 500
            }
        }), 500

@doctors_bp.route('/<int:doctor_id>', methods=['DELETE'])
def delete_doctor(doctor_id):
    """Delete doctor by ID"""
    try:
        db = get_db()
        doctors = db.get('doctors', [])
        doctor_index = next((i for i, d in enumerate(doctors) if d.get('id') == doctor_id), None)
        
        if doctor_index is None:
            return jsonify({
                'error': {
                    'message': 'Doctor not found',
                    'status': 404
                }
            }), 404
        
        deleted_doctor = doctors.pop(doctor_index)
        db['doctors'] = doctors
        save_db(db)
        
        return jsonify({
            'message': 'Doctor deleted successfully',
            'doctor': deleted_doctor
        }), 200
    except Exception as e:
        print(f'Delete doctor error: {e}')
        return jsonify({
            'error': {
                'message': 'Failed to delete doctor',
                'status': 500
            }
        }), 500
