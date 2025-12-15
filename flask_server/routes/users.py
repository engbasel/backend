from flask import Blueprint, request, jsonify
from utils.database import get_users, save_users
from utils.auth import auth_required, admin_required

users_bp = Blueprint('users', __name__)

@users_bp.route('/', methods=['GET'])
@auth_required
@admin_required
def get_all_users():
    """Get all users (admin only)"""
    try:
        users = get_users()
        # Remove passwords from response
        users_response = [{k: v for k, v in user.items() if k != 'password'} for user in users]
        return jsonify(users_response)
    except Exception as e:
        print(f'Get users error: {e}')
        return jsonify({
            'error': {
                'message': 'Failed to retrieve users',
                'status': 500
            }
        }), 500

@users_bp.route('/me', methods=['GET'])
@auth_required
def get_current_user():
    """Get current user profile"""
    try:
        users = get_users()
        user = next((u for u in users if u['id'] == request.user['id']), None)
        
        if not user:
            return jsonify({
                'error': {
                    'message': 'User not found',
                    'status': 404
                }
            }), 404
        
        # Return user without password
        user_response = {k: v for k, v in user.items() if k != 'password'}
        return jsonify(user_response)
    except Exception as e:
        print(f'Get user profile error: {e}')
        return jsonify({
            'error': {
                'message': 'Failed to retrieve user profile',
                'status': 500
            }
        }), 500

@users_bp.route('/<int:user_id>', methods=['PATCH'])
@auth_required
def update_user(user_id):
    """Update user profile"""
    try:
        # Check if user is updating their own profile
        if request.user['id'] != user_id:
            return jsonify({
                'error': {
                    'message': 'Unauthorized to update this profile',
                    'status': 403
                }
            }), 403
        
        data = request.get_json()
        users = get_users()
        
        # Find user
        user = next((u for u in users if u['id'] == user_id), None)
        
        if not user:
            return jsonify({
                'error': {
                    'message': 'User not found',
                    'status': 404
                }
            }), 404
        
        # Update allowed fields
        allowed_fields = ['name', 'phone', 'email']
        for field in allowed_fields:
            if field in data:
                user[field] = data[field]
        
        # Save updated users
        save_users(users)
        
        # Return updated user without password
        user_response = {k: v for k, v in user.items() if k != 'password'}
        return jsonify(user_response)
    except Exception as e:
        print(f'Update user error: {e}')
        import traceback
        traceback.print_exc()
        return jsonify({
            'error': {
                'message': 'Failed to update user profile',
                'status': 500
            }
        }), 500
