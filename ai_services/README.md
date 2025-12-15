# NeuroAid AI Services

This directory contains the AI microservices for the NeuroAid application.

## Services Overview

### 1. Chatbot Service (Port 5001)
- **Purpose**: AI-powered chatbot for stroke-related questions
- **Endpoint**: `POST http://localhost:5001/chat`
- **Features**:
  - Arabic language support
  - Answers questions about stroke symptoms, prevention, risk factors, and treatment
  - Conversation history support

### 2. Stroke Assessment Service (Port 5002)
- **Purpose**: Risk assessment based on patient data
- **Endpoint**: `POST http://localhost:5002/predict`
- **Features**:
  - Comprehensive risk calculation
  - Personalized Arabic recommendations
  - Considers age, gender, health conditions, lifestyle factors

### 3. Stroke Image Analysis Service (Port 5003)
- **Purpose**: Brain scan image analysis
- **Endpoint**: `POST http://localhost:5003/analyze`
- **Features**:
  - Image upload and analysis
  - Confidence scoring
  - Detailed findings in Arabic
  - Support for ML models (TensorFlow/Keras)

## Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Setup Each Service

#### 1. Chatbot Service
```bash
cd chatbot
pip install -r requirements.txt
python app.py
```

#### 2. Stroke Assessment Service
```bash
cd stroke_assessment
pip install -r requirements.txt
python app.py
```

#### 3. Stroke Image Analysis Service
```bash
cd stroke_image
pip install -r requirements.txt
python app.py
```

## Quick Start - Run All Services

Use the provided batch file to start all services at once:

```bash
# From the ai_services directory
start_all_services.bat
```

Or manually start each service in separate terminals.

## API Documentation

### Chatbot API

**Endpoint**: `POST /chat`

**Request Body**:
```json
{
  "message": "ما هي أعراض السكتة الدماغية؟",
  "history": []
}
```

**Response**:
```json
{
  "response": "أعراض السكتة الدماغية الرئيسية تشمل...",
  "timestamp": "2024-12-07T19:30:00",
  "service": "chatbot"
}
```

### Stroke Assessment API

**Endpoint**: `POST /predict`

**Request Body**:
```json
{
  "age": 65,
  "gender": "Male",
  "hypertension": 1,
  "heart_disease": 0,
  "ever_married": "Yes",
  "work_type": "Private",
  "Residence_type": "Urban",
  "avg_glucose_level": 120,
  "bmi": 28,
  "smoking_status": "formerly smoked"
}
```

**Response**:
```json
{
  "risk_level": "medium",
  "risk_percentage": 55,
  "recommendations": [
    "راقب ضغط الدم يومياً...",
    "مارس الرياضة بانتظام..."
  ],
  "timestamp": "2024-12-07T19:30:00",
  "service": "stroke_assessment"
}
```

### Stroke Image Analysis API

**Endpoint**: `POST /analyze`

**Request**: Multipart form data with image file

**Response**:
```json
{
  "result": "normal",
  "confidence": 0.85,
  "findings": [
    "لا توجد علامات واضحة للسكتة الدماغية",
    "الصورة تبدو طبيعية بشكل عام"
  ],
  "timestamp": "2024-12-07T19:30:00",
  "service": "stroke_image_analysis"
}
```

## Integration with Backend

The main backend server (Node.js/Express) at `http://localhost:3001` automatically routes requests to these AI services:

- `/api/ai/chat` → Chatbot Service
- `/api/ai/stroke-assessment` → Stroke Assessment Service
- `/api/ai/scan-image` → Stroke Image Analysis Service

The backend handles:
- Authentication
- Request validation
- Error handling
- Fallback responses if AI services are unavailable

## Environment Variables

Each service can be configured with environment variables:

```env
PORT=5001  # Service port (5001, 5002, or 5003)
DEBUG=True # Enable debug mode
```

## Health Checks

Each service provides a health check endpoint:

```bash
# Chatbot
curl http://localhost:5001/health

# Stroke Assessment
curl http://localhost:5002/health

# Stroke Image Analysis
curl http://localhost:5003/health
```

## Adding ML Models

### Stroke Assessment Model
Place your trained scikit-learn model as `stroke_model.pkl` in the `stroke_assessment` directory.

### Image Analysis Model
Place your trained Keras/TensorFlow model as `stroke_image_model.h5` in the `stroke_image` directory.

If models are not found, services will use rule-based fallback logic.

## Troubleshooting

### Port Already in Use
If a port is already in use, you can change it:
```bash
PORT=5011 python app.py
```

### Dependencies Issues
Make sure you're using compatible versions:
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### CORS Issues
All services have CORS enabled by default. If you need to restrict origins, modify the CORS configuration in each `app.py`.

## Development

### Adding New Features
1. Modify the respective `app.py` file
2. Update the API documentation above
3. Test the endpoint
4. Update the main backend routes if needed

### Testing
Test each service independently:
```bash
# Test chatbot
curl -X POST http://localhost:5001/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "مرحبا"}'

# Test assessment
curl -X POST http://localhost:5002/predict \
  -H "Content-Type: application/json" \
  -d '{"age": 65, "gender": "Male"}'

# Test image analysis
curl -X POST http://localhost:5003/analyze \
  -F "image=@test_image.jpg"
```

## Production Deployment

For production:
1. Set `DEBUG=False`
2. Use a production WSGI server (gunicorn, uWSGI)
3. Set up proper logging
4. Configure reverse proxy (nginx)
5. Enable HTTPS
6. Set up monitoring and health checks

Example with gunicorn:
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5001 app:app
```

## License

Part of the NeuroAid project.
