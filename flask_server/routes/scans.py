from flask import Blueprint, request, jsonify, current_app
from werkzeug.utils import secure_filename
from utils.database import get_db, save_db, get_next_id
from utils.auth import auth_required
from datetime import datetime
import os

scans_bp = Blueprint('scans', __name__)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@scans_bp.route('/', methods=['GET'])
@auth_required
def get_scans():
    """Get user's scans"""
    try:
        db = get_db()
        scans = db.get('scans', [])
        
        # Filter scans for current user
        user_scans = [s for s in scans if s.get('userId') == request.user['id']]
        
        # Sort by date (newest first)
        user_scans.sort(key=lambda x: x.get('createdAt', ''), reverse=True)
        
        return jsonify({
            'scans': user_scans,
            'total': len(user_scans)
        })
    except Exception as e:
        print(f'Get scans error: {e}')
        return jsonify({
            'error': {
                'message': 'Failed to retrieve scans',
                'status': 500
            }
        }), 500

@scans_bp.route('/', methods=['POST'])
@auth_required
def upload_scan():
    """Upload a new scan and analyze it with AI"""
    import requests
    from io import BytesIO

    try:
        # Debug logging
        print(f'[DEBUG] Content-Type: {request.content_type}')
        print(f'[DEBUG] request.files: {request.files}')
        print(f'[DEBUG] request.form: {request.form}')
        print(f'[DEBUG] request.data length: {len(request.data)}')
        print(f'[DEBUG] request.headers: {dict(request.headers)}')
        
        # Check for file with both possible names (scan or image)
        file = None
        if 'scan' in request.files:
            file = request.files['scan']
            print(f'[DEBUG] File found with key: scan')
        elif 'image' in request.files:
            file = request.files['image']
            print(f'[DEBUG] File found with key: image')
        else:
            # List all available keys for debugging
            available_keys = list(request.files.keys())
            print(f'[DEBUG] Available file keys: {available_keys}')
            return jsonify({
                'error': {
                    'message': 'No image file provided',
                    'status': 400,
                    'debug': {
                        'available_keys': available_keys,
                        'expected_keys': ['scan', 'image']
                    }
                }
            }), 400

        if file.filename == '':
            return jsonify({
                'error': {
                    'message': 'No image file selected',
                    'status': 400
                }
            }), 400

        if not allowed_file(file.filename):
            return jsonify({
                'error': {
                    'message': 'Invalid file type. Only images are allowed.',
                    'status': 400
                }
            }), 400

        # Save file
        filename = secure_filename(file.filename)
        timestamp = int(datetime.now().timestamp() * 1000)
        unique_filename = f"scan-{timestamp}-{filename}"

        upload_path = os.path.join(current_app.config['UPLOAD_FOLDER'], 'scans', unique_filename)
        os.makedirs(os.path.dirname(upload_path), exist_ok=True)
        file.save(upload_path)

        image_url = f"/uploads/scans/{unique_filename}"

        # Call AI Image Analysis Service
        ai_result = None
        result = 'unknown'
        confidence = 0.0
        findings = ['تعذر تحليل الصورة']

        try:
            # Read the saved file and send it to AI service
            with open(upload_path, 'rb') as img_file:
                files = {'image': (unique_filename, img_file, 'image/jpeg')}
                ai_response = requests.post(
                    'http://localhost:5003/analyze',
                    files=files,
                    timeout=30
                )

                if ai_response.status_code == 200:
                    ai_result = ai_response.json()
                    result = ai_result.get('result', 'unknown')
                    confidence = ai_result.get('confidence', 0.0)
                    findings = ai_result.get('findings', [])
                else:
                    print(f'AI service error: {ai_response.status_code} - {ai_response.text}')
                    # Use fallback values
                    result = 'analysis_failed'
                    confidence = 0.0
                    findings = ['فشل تحليل الصورة بواسطة نموذج الذكاء الاصطناعي', 'يرجى المحاولة مرة أخرى']
        except Exception as ai_error:
            print(f'AI service connection error: {ai_error}')
            # Use fallback values
            result = 'analysis_failed'
            confidence = 0.0
            findings = ['تعذر الاتصال بخدمة التحليل', 'يرجى التأكد من تشغيل جميع الخدمات']

        # Save to database
        db = get_db()
        scans = db.get('scans', [])

        new_scan = {
            'id': get_next_id(scans),
            'userId': request.user['id'],
            'imageUrl': image_url,
            'result': result,
            'confidence': confidence,
            'findings': findings,
            'createdAt': datetime.now().isoformat(),
            'model': ai_result.get('model') if ai_result else None,
            'source': ai_result.get('source') if ai_result else 'fallback'
        }

        scans.append(new_scan)
        db['scans'] = scans
        save_db(db)

        return jsonify(new_scan), 201
    except Exception as e:
        print(f'Upload scan error: {e}')
        import traceback
        traceback.print_exc()
        return jsonify({
            'error': {
                'message': 'Failed to upload scan',
                'status': 500
            }
        }), 500

@scans_bp.route('/<int:scan_id>', methods=['DELETE'])
@auth_required
def delete_scan(scan_id):
    """Delete a scan"""
    try:
        db = get_db()
        scans = db.get('scans', [])
        
        # Find scan
        scan = next((s for s in scans if s.get('id') == scan_id), None)
        
        if not scan:
            return jsonify({
                'error': {
                    'message': 'Scan not found',
                    'status': 404
                }
            }), 404
        
        # Check if user owns this scan
        if scan.get('userId') != request.user['id']:
            return jsonify({
                'error': {
                    'message': 'Unauthorized to delete this scan',
                    'status': 403
                }
            }), 403
        
        # Delete file if exists
        if scan.get('imageUrl'):
            file_path = os.path.join(
                current_app.config['UPLOAD_FOLDER'],
                scan['imageUrl'].replace('/uploads/', '')
            )
            if os.path.exists(file_path):
                os.remove(file_path)
        
        # Remove from database
        scans = [s for s in scans if s.get('id') != scan_id]
        db['scans'] = scans
        save_db(db)
        
        return jsonify({'message': 'Scan deleted successfully'})
    except Exception as e:
        print(f'Delete scan error: {e}')
        return jsonify({
            'error': {
                'message': 'Failed to delete scan',
                'status': 500
            }
        }), 500
