"""
NeuroAid Stroke Image Analysis Service
=======================================
REAL AI-powered stroke detection from CT/MRI scans.
This service uses the TRAINED Keras model for image analysis.

IMPORTANT: This service uses the TRAINED AI MODEL, NOT mock/rule-based analysis.
"""

import sys
import os

# Fix Windows encoding issues - MUST BE FIRST
if sys.platform == 'win32':
    import codecs
    if sys.stdout.encoding != 'utf-8':
        sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    if sys.stderr.encoding != 'utf-8':
        sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')
    os.environ['PYTHONIOENCODING'] = 'utf-8'

# Add the ai/stroke_image directory to Python path to load the AI model
stroke_image_ai_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', 'ai', 'stroke_image'))
if stroke_image_ai_path not in sys.path:
    sys.path.insert(0, stroke_image_ai_path)

from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime
import numpy as np
from PIL import Image
import io

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

# Load the REAL AI model
model = None
MODEL_LOADED = False
MODEL_PATH = os.path.join(stroke_image_ai_path, 'stroke_image.keras')

try:
    import tensorflow as tf

    if os.path.exists(MODEL_PATH):
        model = tf.keras.models.load_model(MODEL_PATH)
        MODEL_LOADED = True
        print(f"✅ Stroke Image AI Model loaded successfully from: {MODEL_PATH}")
    else:
        print(f"❌ Model file not found at: {MODEL_PATH}")
        print("⚠️  Service will return errors instead of mock responses")
except Exception as e:
    print(f"❌ Failed to load Stroke Image AI Model: {e}")
    print("⚠️  Service will return errors instead of mock responses")

def preprocess_image(image_file):
    """
    Preprocess image for the trained Keras model

    Expected input: CT/MRI scan image
    Output: Preprocessed numpy array ready for model inference
    """
    try:
        # Read image
        image = Image.open(image_file)

        # Convert to RGB if necessary
        if image.mode != 'RGB':
            image = image.convert('RGB')

        # Resize to model's expected input size (adjust based on your model)
        # Common sizes: 224x224, 256x256, or 512x512
        target_size = (224, 224)  # Adjust if your model expects different size
        image = image.resize(target_size)

        # Convert to numpy array and normalize
        img_array = np.array(image).astype('float32')
        img_array = img_array / 255.0  # Normalize to [0, 1]

        # Add batch dimension
        img_array = np.expand_dims(img_array, axis=0)

        return img_array

    except Exception as e:
        raise Exception(f"Error preprocessing image: {str(e)}")

def interpret_prediction(prediction_value):
    """
    Interpret model prediction and return meaningful results

    Args:
        prediction_value: Raw model output (probability)

    Returns:
        result, confidence, findings
    """
    confidence = float(prediction_value)

    # Threshold-based classification
    if confidence > 0.7:
        result = 'abnormal'
        findings = [
            '⚠️ تم اكتشاف علامات محتملة للسكتة الدماغية',
            'توجد مناطق غير طبيعية في الصورة',
            'يُنصح بمراجعة الطبيب المختص فوراً',
            'قد تكون هناك حاجة لفحوصات إضافية',
            'الوقت عامل حاسم في علاج السكتة الدماغية'
        ]
    elif confidence > 0.4:
        result = 'requires_review'
        findings = [
            'الصورة تحتاج إلى مراجعة من قبل أخصائي',
            'توجد بعض المناطق التي تحتاج تقييم دقيق',
            'يُنصح بإجراء فحوصات إضافية للتأكد',
            'استشر طبيب الأعصاب للحصول على تقييم شامل'
        ]
    else:
        result = 'normal'
        findings = [
            '✅ لا توجد علامات واضحة للسكتة الدماغية',
            'الصورة تبدو طبيعية بشكل عام',
            'استمر في المتابعة الدورية مع طبيبك',
            'حافظ على نمط حياة صحي للوقاية'
        ]

    return result, confidence, findings

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'OK' if MODEL_LOADED else 'ERROR',
        'service': 'NeuroAid Stroke Image Analysis Service',
        'ai_model_loaded': MODEL_LOADED,
        'model_path': MODEL_PATH if MODEL_LOADED else None,
        'timestamp': datetime.now().isoformat()
    })

@app.route('/analyze', methods=['POST'])
def analyze():
    """
    REAL AI Image Analysis endpoint - Uses trained Keras model

    Expected input:
    - multipart/form-data with 'image' field containing CT/MRI scan

    Returns: JSON with analysis results from the trained model
    """
    try:
        # Check if AI model is loaded
        if not MODEL_LOADED:
            return jsonify({
                'error': 'AI model not loaded',
                'message': 'The trained stroke image analysis model could not be loaded. Please check server configuration.',
                'details': f'Model file not found at: {MODEL_PATH}'
            }), 503

        # Check if image file is present
        if 'image' not in request.files:
            return jsonify({
                'error': 'No image file provided',
                'message': 'Please provide an image file in the request'
            }), 400

        image_file = request.files['image']

        if image_file.filename == '':
            return jsonify({
                'error': 'No image file selected',
                'message': 'Please select a valid image file'
            }), 400

        # Preprocess image for the model
        try:
            preprocessed_image = preprocess_image(image_file)
        except Exception as preprocess_error:
            return jsonify({
                'error': 'Image preprocessing failed',
                'message': str(preprocess_error)
            }), 400

        # Run inference with the TRAINED MODEL
        try:
            prediction = model.predict(preprocessed_image, verbose=0)
            prediction_value = prediction[0][0]  # Get scalar value

        except Exception as model_error:
            # If the model fails, return error (DO NOT use fallback)
            return jsonify({
                'error': 'AI model inference failed',
                'message': f'The trained model could not analyze the image: {str(model_error)}',
                'details': 'Check that the image format is compatible with the model'
            }), 500

        # Interpret results
        result, confidence, findings = interpret_prediction(prediction_value)

        return jsonify({
            'result': result,
            'confidence': round(confidence, 3),
            'findings': findings,
            'timestamp': datetime.now().isoformat(),
            'service': 'stroke_image_analysis',
            'model': 'keras_cnn',
            'source': 'trained_ai_model'
        })

    except Exception as e:
        return jsonify({
            'error': 'Server error',
            'message': str(e)
        }), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5003))
    print(f"\n{'='*60}")
    print(f"🔬 NeuroAid Stroke Image Analysis Service (REAL AI MODEL)")
    print(f"{'='*60}")
    print(f"📍 Running on: http://localhost:{port}")
    print(f"📍 Health check: http://localhost:{port}/health")
    print(f"�� Analyze endpoint: POST http://localhost:{port}/analyze")
    print(f"🧠 AI Model: {'LOADED ✅' if MODEL_LOADED else 'NOT LOADED ❌'}")
    print(f"{'='*60}\n")

    if not MODEL_LOADED:
        print("⚠️  WARNING: AI model not loaded. Service will return errors.")
        print(f"⚠️  Check that model file exists at: {MODEL_PATH}")
        print("⚠️  Expected file: stroke_image.keras\n")

    app.run(host='0.0.0.0', port=port, debug=True)
