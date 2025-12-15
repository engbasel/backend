from flask import Blueprint, request, jsonify, current_app
from werkzeug.utils import secure_filename
from utils.auth import auth_required
from datetime import datetime
import requests
import os

ai_bp = Blueprint('ai', __name__)

# AI Services URLs
AI_CHATBOT_URL = os.getenv('AI_CHATBOT_URL', 'http://localhost:5001')
AI_STROKE_QA_URL = os.getenv('AI_STROKE_QA_URL', 'http://localhost:5002')
AI_STROKE_IMAGE_URL = os.getenv('AI_STROKE_IMAGE_URL', 'http://localhost:5003')

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@ai_bp.route('/chat', methods=['POST'])
@auth_required
def chat():
    """
    AI Chatbot endpoint - Forwards to REAL AI model service

    IMPORTANT: This endpoint ONLY forwards to the trained AI model.
    NO fallback responses. If the AI service fails, it returns an error.
    """
    try:
        data = request.get_json()
        message = data.get('message')

        if not message:
            return jsonify({
                'error': {
                    'message': 'Message is required',
                    'status': 400
                }
            }), 400

        conversation_history = data.get('conversationHistory', [])

        # Forward to AI service (REQUIRED - no fallback)
        try:
            response = requests.post(
                f'{AI_CHATBOT_URL}/chat',
                json={
                    'message': message,
                    'history': conversation_history
                },
                timeout=60
            )

            # Return the response from the AI model (could be success or error)
            return jsonify(response.json()), response.status_code

        except requests.exceptions.ConnectionError as e:
            print(f'AI Chatbot service connection error: {e}')
            return jsonify({
                'error': {
                    'message': 'AI service unavailable',
                    'details': 'Could not connect to the AI chatbot service. Please ensure the service is running on port 5001.',
                    'status': 503
                }
            }), 503

        except requests.exceptions.Timeout as e:
            print(f'AI Chatbot service timeout: {e}')
            return jsonify({
                'error': {
                    'message': 'AI service timeout',
                    'details': 'The AI model took too long to respond. Please try again.',
                    'status': 504
                }
            }), 504

        except Exception as e:
            print(f'AI Chatbot service error: {e}')
            return jsonify({
                'error': {
                    'message': 'AI service error',
                    'details': str(e),
                    'status': 500
                }
            }), 500

    except Exception as e:
        print(f'Chat endpoint error: {e}')
        return jsonify({
            'error': {
                'message': 'Failed to process chat message',
                'details': str(e),
                'status': 500
            }
        }), 500

@ai_bp.route('/stroke-assessment', methods=['POST'])
@auth_required
def stroke_assessment():
    """Stroke Risk Assessment endpoint"""
    try:
        data = request.get_json()
        
        age = data.get('age')
        gender = data.get('gender')
        
        if not age or not gender:
            return jsonify({
                'error': {
                    'message': 'Age and gender are required',
                    'status': 400
                }
            }), 400
        
        # Prepare data for AI service
        assessment_data = {
            'age': age,
            'gender': gender,
            'hypertension': data.get('hypertension', 0),
            'heart_disease': data.get('heartDisease', 0),
            'ever_married': data.get('everMarried', 'No'),
            'work_type': data.get('workType', 'Private'),
            'Residence_type': data.get('residenceType', 'Urban'),
            'avg_glucose_level': data.get('avgGlucoseLevel', 100),
            'bmi': data.get('bmi', 25),
            'smoking_status': data.get('smokingStatus', 'never smoked')
        }
        
        # Try to connect to AI service
        try:
            response = requests.post(
                f'{AI_STROKE_QA_URL}/predict',
                json=assessment_data,
                timeout=30
            )
            
            if response.status_code == 200:
                return jsonify(response.json())
        except Exception as e:
            print(f'AI Stroke QA service error: {e}')
        
        # Mock risk calculation when AI service is not available
        risk_score = 0
        
        # Age factor
        if age > 65:
            risk_score += 30
        elif age > 55:
            risk_score += 20
        elif age > 45:
            risk_score += 10
        
        # Health conditions
        if data.get('hypertension'):
            risk_score += 25
        if data.get('heartDisease'):
            risk_score += 25
        
        # Lifestyle factors
        smoking_status = data.get('smokingStatus', 'never smoked')
        if smoking_status in ['smokes', 'formerly smoked']:
            risk_score += 15
        
        bmi = data.get('bmi', 25)
        if bmi > 30:
            risk_score += 10
        
        avg_glucose = data.get('avgGlucoseLevel', 100)
        if avg_glucose > 140:
            risk_score += 10
        
        risk_percentage = min(risk_score, 100)
        
        if risk_percentage > 70:
            risk_level = 'high'
        elif risk_percentage > 40:
            risk_level = 'medium'
        else:
            risk_level = 'low'
        
        recommendations = [
            'استشر طبيبك في أقرب وقت ممكن' if risk_level == 'high' else 'حافظ على نمط حياة صحي',
            'مارس الرياضة بانتظام لمدة 30 دقيقة يومياً',
            'اتبع نظام غذائي صحي غني بالخضروات والفواكه',
            'راقب ضغط الدم بانتظام' if data.get('hypertension') else 'افحص ضغط الدم دورياً',
            'توقف عن التدخين فوراً' if smoking_status == 'smokes' else 'تجنب التدخين السلبي'
        ]
        
        return jsonify({
            'riskLevel': risk_level,
            'riskPercentage': risk_percentage,
            'recommendations': recommendations,
            'timestamp': datetime.now().isoformat(),
            'note': 'This is a mock assessment. AI service integration pending.'
        })
    
    except Exception as e:
        print(f'Stroke assessment error: {e}')
        return jsonify({
            'error': {
                'message': 'Failed to assess stroke risk',
                'status': 500
            }
        }), 500

@ai_bp.route('/scan-image', methods=['POST'])
@auth_required
def scan_image():
    """
    Scan Image Analysis endpoint - Forwards to REAL AI model service

    IMPORTANT: This endpoint ONLY forwards to the trained AI image model.
    NO fallback responses. If the AI service fails, it returns an error.
    """
    try:
        if 'image' not in request.files:
            return jsonify({
                'error': {
                    'message': 'Image file is required',
                    'status': 400
                }
            }), 400

        file = request.files['image']

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
                    'message': 'Invalid file type. Allowed: png, jpg, jpeg, gif',
                    'status': 400
                }
            }), 400

        # Save file temporarily for record keeping
        filename = secure_filename(file.filename)
        timestamp = int(datetime.now().timestamp() * 1000)
        unique_filename = f"scan-{timestamp}-{filename}"

        upload_path = os.path.join(current_app.config['UPLOAD_FOLDER'], 'scans', unique_filename)
        os.makedirs(os.path.dirname(upload_path), exist_ok=True)
        file.save(upload_path)

        image_url = f"/uploads/scans/{unique_filename}"

        # Forward to AI service (REQUIRED - no fallback)
        try:
            with open(upload_path, 'rb') as img_file:
                files = {'image': (filename, img_file, file.content_type)}
                response = requests.post(
                    f'{AI_STROKE_IMAGE_URL}/analyze',
                    files=files,
                    timeout=60
                )

                # Return the response from the AI model (could be success or error)
                if response.status_code == 200:
                    result_data = response.json()
                    result_data['scanId'] = timestamp
                    result_data['imageUrl'] = image_url
                    return jsonify(result_data), 200
                else:
                    # Return AI service error
                    return jsonify(response.json()), response.status_code

        except requests.exceptions.ConnectionError as e:
            print(f'AI Stroke Image service connection error: {e}')
            return jsonify({
                'error': {
                    'message': 'AI image analysis service unavailable',
                    'details': 'Could not connect to the AI image analysis service. Please ensure the service is running on port 5003.',
                    'status': 503
                }
            }), 503

        except requests.exceptions.Timeout as e:
            print(f'AI Stroke Image service timeout: {e}')
            return jsonify({
                'error': {
                    'message': 'AI service timeout',
                    'details': 'The AI model took too long to analyze the image. Please try again.',
                    'status': 504
                }
            }), 504

        except Exception as e:
            print(f'AI Stroke Image service error: {e}')
            return jsonify({
                'error': {
                    'message': 'AI service error',
                    'details': str(e),
                    'status': 500
                }
            }), 500

    except Exception as e:
        print(f'Scan image endpoint error: {e}')
        return jsonify({
            'error': {
                'message': 'Failed to process image',
                'details': str(e),
                'status': 500
            }
        }), 500
