import sys
import os

# Fix Windows encoding issues - MUST BE FIRST
if sys.platform == 'win32':
    import codecs
    # Force UTF-8 for stdout and stderr
    if sys.stdout.encoding != 'utf-8':
        sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    if sys.stderr.encoding != 'utf-8':
        sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')
    os.environ['PYTHONIOENCODING'] = 'utf-8'

from flask import Flask, request, jsonify
from flask_cors import CORS
import pickle
import numpy as np
from datetime import datetime

app = Flask(__name__)
# CORS Configuration for LAN Access
CORS(app, resources={r"/*": {"origins": "*"}})

# Load the trained model (if exists)
MODEL_PATH = 'stroke_model.pkl'
model = None

try:
    if os.path.exists(MODEL_PATH):
        with open(MODEL_PATH, 'rb') as f:
            model = pickle.load(f)
        print(f"✅ Model loaded from {MODEL_PATH}")
except Exception as e:
    print(f"⚠️  Could not load model: {e}")
    print("Using rule-based assessment instead")

def calculate_risk_rule_based(data):
    """Calculate stroke risk using rule-based approach"""
    risk_score = 0
    
    # Age factor (0-30 points)
    age = float(data.get('age', 0))
    if age > 75:
        risk_score += 30
    elif age > 65:
        risk_score += 25
    elif age > 55:
        risk_score += 20
    elif age > 45:
        risk_score += 15
    elif age > 35:
        risk_score += 10
    
    # Gender factor (males slightly higher risk)
    gender = data.get('gender', 'Male')
    if gender == 'Male':
        risk_score += 5
    
    # Hypertension (0-25 points)
    if int(data.get('hypertension', 0)) == 1:
        risk_score += 25
    
    # Heart disease (0-25 points)
    if int(data.get('heart_disease', 0)) == 1:
        risk_score += 25
    
    # Glucose level (0-15 points)
    glucose = float(data.get('avg_glucose_level', 100))
    if glucose > 200:
        risk_score += 15
    elif glucose > 140:
        risk_score += 10
    elif glucose > 100:
        risk_score += 5
    
    # BMI (0-10 points)
    bmi = float(data.get('bmi', 25))
    if bmi > 35:
        risk_score += 10
    elif bmi > 30:
        risk_score += 7
    elif bmi > 25:
        risk_score += 3
    
    # Smoking status (0-15 points)
    smoking = data.get('smoking_status', 'never smoked')
    if smoking == 'smokes':
        risk_score += 15
    elif smoking == 'formerly smoked':
        risk_score += 10
    
    # Work type (stress factor)
    work_type = data.get('work_type', 'Private')
    if work_type == 'Self-employed':
        risk_score += 5
    elif work_type == 'Govt_job':
        risk_score += 3
    
    # Cap at 100
    risk_percentage = min(risk_score, 100)
    
    # Determine risk level
    if risk_percentage >= 70:
        risk_level = 'high'
    elif risk_percentage >= 40:
        risk_level = 'medium'
    else:
        risk_level = 'low'
    
    return risk_level, risk_percentage

def get_recommendations(risk_level, data):
    """Get personalized recommendations based on risk level and data"""
    recommendations = []
    
    # Critical recommendations for high risk
    if risk_level == 'high':
        recommendations.append('⚠️ استشر طبيبك في أقرب وقت ممكن - مستوى الخطر مرتفع')
        recommendations.append('📞 احتفظ بأرقام الطوارئ في متناول يدك')
    
    # Age-based
    age = float(data.get('age', 0))
    if age > 65:
        recommendations.append('👴 نظراً لعمرك، احرص على الفحوصات الدورية المنتظمة')
    
    # Hypertension
    if int(data.get('hypertension', 0)) == 1:
        recommendations.append('💊 راقب ضغط الدم يومياً والتزم بالأدوية الموصوفة')
        recommendations.append('🧂 قلل من تناول الملح والأطعمة المصنعة')
    else:
        recommendations.append('📊 افحص ضغط الدم بانتظام كل 3-6 أشهر')
    
    # Heart disease
    if int(data.get('heart_disease', 0)) == 1:
        recommendations.append('❤️ تابع مع طبيب القلب بانتظام')
        recommendations.append('💊 التزم بأدوية القلب الموصوفة')
    
    # Glucose
    glucose = float(data.get('avg_glucose_level', 100))
    if glucose > 140:
        recommendations.append('🍬 راقب مستوى السكر في الدم وقلل من السكريات')
        recommendations.append('🥗 اتبع نظام غذائي منخفض السكر')
    elif glucose > 100:
        recommendations.append('📉 انتبه لمستوى السكر وقلل من الحلويات')
    
    # BMI
    bmi = float(data.get('bmi', 25))
    if bmi > 30:
        recommendations.append('⚖️ اعمل على تقليل الوزن تدريجياً بنظام صحي')
        recommendations.append('🏃 مارس الرياضة 30-45 دقيقة يومياً')
    elif bmi > 25:
        recommendations.append('🚶 حافظ على نشاط بدني منتظم لتجنب زيادة الوزن')
    
    # Smoking
    smoking = data.get('smoking_status', 'never smoked')
    if smoking == 'smokes':
        recommendations.append('🚭 توقف عن التدخين فوراً - أهم خطوة للوقاية')
        recommendations.append('💪 اطلب المساعدة الطبية للإقلاع عن التدخين')
    elif smoking == 'formerly smoked':
        recommendations.append('✅ ممتاز! استمر في الابتعاد عن التدخين')
    else:
        recommendations.append('🌟 تجنب التدخين السلبي والبيئات المدخنة')
    
    # General recommendations
    recommendations.append('🥗 اتبع نظام غذائي صحي غني بالخضروات والفواكه')
    recommendations.append('💧 اشرب كمية كافية من الماء يومياً (8 أكواب)')
    recommendations.append('😴 احصل على نوم كافٍ (7-8 ساعات يومياً)')
    recommendations.append('🧘 قلل من التوتر بممارسة التأمل أو اليوغا')
    
    if risk_level == 'low':
        recommendations.append('✨ حافظ على نمط حياتك الصحي الحالي')
    
    return recommendations

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'OK',
        'service': 'NeuroAid Stroke Assessment Service',
        'model_loaded': model is not None,
        'timestamp': datetime.now().isoformat()
    })

@app.route('/predict', methods=['POST'])
def predict():
    """Stroke risk prediction endpoint"""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['age', 'gender']
        for field in required_fields:
            if field not in data:
                return jsonify({
                    'error': f'{field} is required'
                }), 400
        
        # Calculate risk
        risk_level, risk_percentage = calculate_risk_rule_based(data)
        
        # Get recommendations
        recommendations = get_recommendations(risk_level, data)
        
        return jsonify({
            'risk_level': risk_level,
            'risk_percentage': risk_percentage,
            'recommendations': recommendations,
            'timestamp': datetime.now().isoformat(),
            'service': 'stroke_assessment',
            'method': 'rule_based' if model is None else 'ml_model'
        })
    
    except Exception as e:
        return jsonify({
            'error': str(e)
        }), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5002))
    print(f"\n🏥 NeuroAid Stroke Assessment Service")
    print(f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print(f"📍 Running on: http://localhost:{port}")
    print(f"📍 Health check: http://localhost:{port}/health")
    print(f"📍 Predict endpoint: POST http://localhost:{port}/predict")
    print(f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n")
    
    app.run(host='0.0.0.0', port=port, debug=True)
