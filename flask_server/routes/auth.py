from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from utils.database import get_users, save_users, get_next_id
from utils.auth import generate_token
from datetime import datetime

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    """Register a new user"""
    try:
        data = request.get_json()
        
        # Validation
        email = data.get('email')
        password = data.get('password')
        name = data.get('name')
        
        if not email or not password or not name:
            return jsonify({
                'error': {
                    'message': 'Email, password, and name are required',
                    'status': 400
                }
            }), 400
        
        users = get_users()
        
        # Check if user already exists
        if any(u['email'] == email for u in users):
            return jsonify({
                'error': {
                    'message': 'User with this email already exists',
                    'status': 400
                }
            }), 400
        
        # Create new user
        new_user = {
            'id': get_next_id(users),
            'email': email,
            'password': generate_password_hash(password),
            'name': name,
            'phone': data.get('phone', ''),
            'role': data.get('role', 'user'),
            'isActive': True,
            'createdAt': datetime.now().isoformat()
        }
        
        users.append(new_user)
        save_users(users)
        
        # Generate token
        token = generate_token(new_user)
        
        # Return user without password
        user_response = {k: v for k, v in new_user.items() if k != 'password'}
        
        return jsonify({
            'accessToken': token,
            'user': user_response
        }), 201
        
    except Exception as e:
        print(f'Register error: {e}')
        return jsonify({
            'error': {
                'message': 'Registration failed',
                'status': 500
            }
        }), 500

@auth_bp.route('/login', methods=['POST'])
def login():
    """Login user"""
    try:
        data = request.get_json()
        
        # Validation
        email = data.get('email')
        password = data.get('password')
        
        if not email or not password:
            return jsonify({
                'error': {
                    'message': 'Email and password are required',
                    'status': 400
                }
            }), 400
        
        users = get_users()
        user = next((u for u in users if u['email'] == email), None)
        
        if not user:
            return jsonify({
                'error': {
                    'message': 'Invalid email or password',
                    'status': 401
                }
            }), 401
        
        # Check password
        if not check_password_hash(user['password'], password):
            return jsonify({
                'error': {
                    'message': 'Invalid email or password',
                    'status': 401
                }
            }), 401
        
        # Check if user is active
        if not user.get('isActive', True):
            return jsonify({
                'error': {
                    'message': 'Account is deactivated',
                    'status': 403
                }
            }), 403
        
        # Generate token
        token = generate_token(user)
        
        # Return user without password
        user_response = {k: v for k, v in user.items() if k != 'password'}
        
        return jsonify({
            'accessToken': token,
            'user': user_response
        })
        
    except Exception as e:
        print(f'Login error: {e}')
        return jsonify({
            'error': {
                'message': 'Login failed',
                'status': 500
            }
        }), 500
