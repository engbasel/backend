from flask import Blueprint, request, jsonify
from utils.database import get_db, save_db, get_next_id
from utils.auth import auth_required
from datetime import datetime

bookings_bp = Blueprint('bookings', __name__)

@bookings_bp.route('/', methods=['GET'])
@auth_required
def get_bookings():
    """Get user bookings"""
    try:
        db = get_db()
        bookings = db.get('bookings', [])
        doctors = db.get('doctors', [])
        
        # Filter bookings for current user
        user_bookings = [b for b in bookings if b.get('userId') == request.user['id']]
        
        # Add doctor info to each booking
        for booking in user_bookings:
            doctor = next((d for d in doctors if d.get('id') == booking.get('doctorId')), None)
            if doctor:
                booking['doctor'] = {
                    'name': doctor.get('name'),
                    'specialty': doctor.get('specialty')
                }
        
        return jsonify({'bookings': user_bookings})
    except Exception as e:
        print(f'Get bookings error: {e}')
        return jsonify({
            'error': {
                'message': 'Failed to retrieve bookings',
                'status': 500
            }
        }), 500

@bookings_bp.route('/', methods=['POST'])
@auth_required
def create_booking():
    """Create a new booking"""
    try:
        data = request.get_json()
        
        doctor_id = data.get('doctorId')
        date = data.get('date')
        time = data.get('time')
        
        if not doctor_id or not date or not time:
            return jsonify({
                'error': {
                    'message': 'Doctor ID, date, and time are required',
                    'status': 400
                }
            }), 400
        
        db = get_db()
        bookings = db.get('bookings', [])
        
        # Create new booking
        new_booking = {
            'id': get_next_id(bookings),
            'userId': request.user['id'],
            'doctorId': doctor_id,
            'date': date,
            'time': time,
            'status': 'upcoming',
            'notes': data.get('notes', ''),
            'createdAt': datetime.now().isoformat()
        }
        
        bookings.append(new_booking)
        db['bookings'] = bookings
        save_db(db)
        
        return jsonify({'booking': new_booking}), 201
    except Exception as e:
        print(f'Create booking error: {e}')
        return jsonify({
            'error': {
                'message': 'Failed to create booking',
                'status': 500
            }
        }), 500

@bookings_bp.route('/<int:booking_id>', methods=['PATCH'])
@auth_required
def update_booking_status(booking_id):
    """Update booking status"""
    try:
        data = request.get_json()
        new_status = data.get('status')
        
        if not new_status or new_status not in ['upcoming', 'completed', 'canceled']:
            return jsonify({
                'error': {
                    'message': 'Invalid status. Must be: upcoming, completed, or canceled',
                    'status': 400
                }
            }), 400
        
        db = get_db()
        bookings = db.get('bookings', [])
        
        # Find booking
        booking = next((b for b in bookings if b.get('id') == booking_id), None)
        
        if not booking:
            return jsonify({
                'error': {
                    'message': 'Booking not found',
                    'status': 404
                }
            }), 404
        
        # Check if user owns this booking
        if booking.get('userId') != request.user['id']:
            return jsonify({
                'error': {
                    'message': 'Unauthorized to update this booking',
                    'status': 403
                }
            }), 403
        
        # Update status
        booking['status'] = new_status
        booking['updatedAt'] = datetime.now().isoformat()
        
        save_db(db)
        
        return jsonify({'booking': booking})
    except Exception as e:
        print(f'Update booking error: {e}')
        return jsonify({
            'error': {
                'message': 'Failed to update booking',
                'status': 500
            }
        }), 500

@bookings_bp.route('/<int:booking_id>', methods=['DELETE'])
@auth_required
def delete_booking(booking_id):
    """Delete a booking (admin only - for cleanup)"""
    try:
        db = get_db()
        bookings = db.get('bookings', [])
        
        # Find booking
        booking = next((b for b in bookings if b.get('id') == booking_id), None)
        
        if not booking:
            return jsonify({
                'error': {
                    'message': 'Booking not found',
                    'status': 404
                }
            }), 404
        
        # Check if user owns this booking
        if booking.get('userId') != request.user['id']:
            return jsonify({
                'error': {
                    'message': 'Unauthorized to delete this booking',
                    'status': 403
                }
            }), 403
        
        # Remove booking
        bookings = [b for b in bookings if b.get('id') != booking_id]
        db['bookings'] = bookings
        save_db(db)
        
        return jsonify({'message': 'Booking deleted successfully'})
    except Exception as e:
        print(f'Delete booking error: {e}')
        return jsonify({
            'error': {
                'message': 'Failed to delete booking',
                'status': 500
            }
        }), 500
