import jwt
from functools import wraps
from flask import request, jsonify, current_app
from datetime import datetime, timedelta

def generate_token(user_data):
    """Generate JWT token"""
    payload = {
        'id': user_data['id'],
        'email': user_data['email'],
        'role': user_data.get('role', 'user'),
        'exp': datetime.utcnow() + timedelta(days=7)  # 7 days expiration
    }
    
    token = jwt.encode(
        payload,
        current_app.config['SECRET_KEY'],
        algorithm='HS256'
    )
    
    return token

def verify_token(token):
    """Verify JWT token"""
    try:
        payload = jwt.decode(
            token,
            current_app.config['SECRET_KEY'],
            algorithms=['HS256']
        )
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None

def auth_required(f):
    """Decorator to require authentication"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        
        if not auth_header or not auth_header.startswith('Bearer '):
            return jsonify({
                'error': {
                    'message': 'No token provided',
                    'status': 401
                }
            }), 401
        
        token = auth_header[7:]  # Remove 'Bearer ' prefix
        payload = verify_token(token)
        
        if not payload:
            return jsonify({
                'error': {
                    'message': 'Invalid or expired token',
                    'status': 401
                }
            }), 401
        
        # Add user info to request
        request.user = payload
        
        return f(*args, **kwargs)
    
    return decorated_function

def admin_required(f):
    """Decorator to require admin role"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not hasattr(request, 'user') or request.user.get('role') != 'admin':
            return jsonify({
                'error': {
                    'message': 'Access forbidden. Admin only.',
                    'status': 403
                }
            }), 403
        
        return f(*args, **kwargs)
    
    return decorated_function
