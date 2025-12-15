from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from dotenv import load_dotenv
import os
from datetime import datetime

# Load environment variables
load_dotenv()

# Import blueprints
from routes.auth import auth_bp
from routes.users import users_bp
from routes.doctors import doctors_bp
from routes.bookings import bookings_bp
from routes.faqs import faqs_bp
from routes.scans import scans_bp
from routes.favorites import favorites_bp
from routes.ai import ai_bp

# Create Flask app
app = Flask(__name__)
app.url_map.strict_slashes = False  # Allow URLs with or without trailing slashes

# CORS Configuration for LAN Access
CORS(app, resources={
    r"/*": {
        "origins": "*",
        "methods": ["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization", "Accept"],
        "supports_credentials": True
    }
})

# Configuration
app.config['SECRET_KEY'] = os.getenv('JWT_SECRET', 'your-secret-key-change-this-in-production')
app.config['JWT_EXPIRES_IN'] = os.getenv('JWT_EXPIRES_IN', '7d')
app.config['MAX_CONTENT_LENGTH'] = int(os.getenv('MAX_FILE_SIZE', 10 * 1024 * 1024))  # 10MB
app.config['UPLOAD_FOLDER'] = os.getenv('UPLOAD_PATH', './uploads')

# Create uploads directory if it doesn't exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(os.path.join(app.config['UPLOAD_FOLDER'], 'scans'), exist_ok=True)

# Register blueprints
app.register_blueprint(auth_bp, url_prefix='/api/auth')
app.register_blueprint(users_bp, url_prefix='/api/users')
app.register_blueprint(doctors_bp, url_prefix='/api/doctors')
app.register_blueprint(bookings_bp, url_prefix='/api/bookings')
app.register_blueprint(faqs_bp, url_prefix='/api/faqs')
app.register_blueprint(scans_bp, url_prefix='/api/scans')
app.register_blueprint(favorites_bp, url_prefix='/api/favorites')
app.register_blueprint(ai_bp, url_prefix='/api/ai')

# Static files for uploads
@app.route('/uploads/<path:filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

# Health check
@app.route('/health', methods=['GET'])
def health():
    return jsonify({
        'status': 'OK',
        'message': 'NeuroAid Backend Server is running (Flask)',
        'timestamp': datetime.now().isoformat(),
        'services': {
            'auth': 'active',
            'ai': 'active',
            'database': 'active'
        }
    })

# Config endpoint for mobile app
@app.route('/config', methods=['GET'])
def config():
    import socket
    
    # Get local IP address
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        server_ip = s.getsockname()[0]
        s.close()
    except:
        server_ip = 'localhost'
    
    return jsonify({
        'serverIP': server_ip,
        'port': int(os.getenv('PORT', 3001)),
        'environment': os.getenv('NODE_ENV', 'development')
    })

# Error handlers
@app.errorhandler(400)
def bad_request(error):
    return jsonify({
        'error': {
            'message': str(error),
            'status': 400
        }
    }), 400

@app.errorhandler(401)
def unauthorized(error):
    return jsonify({
        'error': {
            'message': 'Unauthorized',
            'status': 401
        }
    }), 401

@app.errorhandler(403)
def forbidden(error):
    return jsonify({
        'error': {
            'message': 'Forbidden',
            'status': 403
        }
    }), 403

@app.errorhandler(404)
def not_found(error):
    return jsonify({
        'error': {
            'message': 'Route not found',
            'status': 404
        }
    }), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({
        'error': {
            'message': 'Internal Server Error',
            'status': 500
        }
    }), 500

if __name__ == '__main__':
    import sys
    # Fix console encoding for Windows
    if sys.platform == 'win32':
        import codecs
        sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
        sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

    port = int(os.getenv('PORT', 5000))

    print('\n>> NeuroAid Backend Server Started (Flask)!')
    print('=' * 50)
    print(f'Server URL: http://localhost:{port}')
    print(f'For Android Emulator: http://10.0.2.2:{port}')
    print(f'Environment: {os.getenv("NODE_ENV", "development")}')
    print('=' * 50)
    print('\nAvailable API Endpoints:')
    print('   GET    /health                    - Health check')
    print('   GET    /config                    - Server configuration')
    print('   POST   /api/auth/register         - Register new user')
    print('   POST   /api/auth/login            - Login user')
    print('   GET    /api/users                 - Get all users')
    print('   GET    /api/users/me              - Get current user')
    print('   POST   /api/ai/chat               - AI Chatbot')
    print('   POST   /api/ai/stroke-assessment  - Stroke Risk Assessment')
    print('   POST   /api/ai/scan-image         - Scan Image Analysis')
    print('   GET    /api/scans                 - Get user scans')
    print('   POST   /api/scans                 - Upload new scan')
    print('   GET    /api/faqs                  - Get FAQs')
    print('   GET    /api/doctors               - Get doctors')
    print('   GET    /api/bookings              - Get bookings')
    print('   POST   /api/bookings              - Create booking')
    print('   GET    /api/favorites             - Get favorites')
    print('=' * 50 + '\n')

    app.run(host='0.0.0.0', port=port, debug=True)
