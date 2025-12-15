# NeuroAid Backend - Testing Guide

## 🧪 Testing the Orchestration System

### Step 1: Install Dependencies

```bash
cd "d:\courses\Flutter\projects\Work\Graduation Projects\Delta\neuroaid\backend"
pip install -r requirements.txt
```

### Step 2: Start the System

**Option A: Using Python Script**
```bash
python run_system.py
```

**Option B: Using Batch File (Windows)**
```bash
start_system.bat
```

### Step 3: Verify All Services are Running

You should see output like:
```
🌐 Starting Main Flask Server on port 5000...
🤖 Starting AI Chatbot Service on port 5001...
🏥 Starting Stroke Assessment Service on port 5002...
🚀 Starting API Gateway on port 8080...

✓ All services started successfully!

API Gateway: http://localhost:8080
Health Check: http://localhost:8080/health
```

## 🔍 Test Endpoints

### 1. Gateway Health Check

**Request:**
```bash
curl http://localhost:8080/health
```

**Expected Response:**
```json
{
  "gateway": "OK",
  "timestamp": "2025-12-13T09:14:02.123456",
  "services": {
    "main": {
      "status": "online",
      "url": "http://localhost:5000"
    },
    "ai_chatbot": {
      "status": "online",
      "url": "http://localhost:5001"
    },
    "ai_assessment": {
      "status": "online",
      "url": "http://localhost:5002"
    }
  }
}
```

### 2. Main Server (Through Gateway)

**Request:**
```bash
curl http://localhost:8080/api/main/health
```

**Expected Response:**
```json
{
  "status": "OK",
  "message": "NeuroAid Backend Server is running (Flask)",
  "timestamp": "2025-12-13T09:14:02.123456",
  "services": {
    "auth": "active",
    "ai": "active",
    "database": "active"
  }
}
```

**Gateway Logs Should Show:**
```
[GATEWAY] 2025-12-13 09:14:02 - Incoming Request: GET /api/main/health
[GATEWAY] Routing to: Main Flask Server
[GATEWAY] Response: 200 - Time: 45.23ms
```

### 3. AI Chatbot (Through Gateway)

**Request:**
```bash
curl -X POST http://localhost:8080/api/ai/chat \
  -H "Content-Type: application/json" \
  -d "{\"message\": \"مرحبا\"}"
```

**Expected Response:**
```json
{
  "response": "مرحباً! أنا مساعدك الذكي في NeuroAid. كيف يمكنني مساعدتك اليوم؟",
  "timestamp": "2025-12-13T09:14:02.123456",
  "service": "chatbot"
}
```

**Gateway Logs Should Show:**
```
[GATEWAY] 2025-12-13 09:14:02 - Incoming Request: POST /api/ai/chat
[GATEWAY] Routing to: AI Chatbot Service
[GATEWAY] Response: 200 - Time: 78.91ms
```

### 4. Stroke Assessment (Through Gateway)

**Request:**
```bash
curl -X POST http://localhost:8080/api/ai/assessment \
  -H "Content-Type: application/json" \
  -d "{
    \"age\": 65,
    \"gender\": \"Male\",
    \"hypertension\": 1,
    \"heart_disease\": 0,
    \"avg_glucose_level\": 150,
    \"bmi\": 28.5,
    \"smoking_status\": \"formerly smoked\"
  }"
```

**Expected Response:**
```json
{
  "risk_level": "medium",
  "risk_percentage": 65,
  "recommendations": [
    "نظراً لعمرك، احرص على الفحوصات الدورية المنتظمة",
    "راقب ضغط الدم يومياً والتزم بالأدوية الموصوفة",
    "..."
  ],
  "timestamp": "2025-12-13T09:14:02.123456",
  "service": "stroke_assessment",
  "method": "rule_based"
}
```

**Gateway Logs Should Show:**
```
[GATEWAY] 2025-12-13 09:14:02 - Incoming Request: POST /api/ai/assessment
[GATEWAY] Routing to: Stroke Assessment Service
[GATEWAY] Response: 200 - Time: 156.42ms
```

## 🛠️ Testing with Postman

### Import Collection

Create a Postman collection with these requests:

1. **Gateway Health**
   - Method: GET
   - URL: `http://localhost:8080/health`

2. **Main Server Health**
   - Method: GET
   - URL: `http://localhost:8080/api/main/health`

3. **Chatbot**
   - Method: POST
   - URL: `http://localhost:8080/api/ai/chat`
   - Body (JSON):
     ```json
     {
       "message": "ما هي أعراض السكتة الدماغية؟"
     }
     ```

4. **Stroke Assessment**
   - Method: POST
   - URL: `http://localhost:8080/api/ai/assessment`
   - Body (JSON):
     ```json
     {
       "age": 55,
       "gender": "Female",
       "hypertension": 0,
       "heart_disease": 0,
       "avg_glucose_level": 110,
       "bmi": 24.5,
       "smoking_status": "never smoked",
       "work_type": "Private"
     }
     ```

## 📱 Testing from Flutter App

### Update Your Flutter Configuration

**Before:**
```dart
// Multiple service URLs
const String MAIN_SERVER = 'http://localhost:5000';
const String CHATBOT_SERVICE = 'http://localhost:5001';
const String ASSESSMENT_SERVICE = 'http://localhost:5002';

// API calls
final mainResponse = await http.get('$MAIN_SERVER/api/auth/login');
final chatResponse = await http.post('$CHATBOT_SERVICE/chat', ...);
final assessResponse = await http.post('$ASSESSMENT_SERVICE/predict', ...);
```

**After:**
```dart
// Single gateway URL
const String API_GATEWAY = 'http://localhost:8080';

// All API calls through gateway
final mainResponse = await http.get('$API_GATEWAY/api/main/auth/login');
final chatResponse = await http.post('$API_GATEWAY/api/ai/chat', ...);
final assessResponse = await http.post('$API_GATEWAY/api/ai/assessment', ...);
```

### For Android Emulator

Use `10.0.2.2` instead of `localhost`:

```dart
const String API_GATEWAY = 'http://10.0.2.2:8080';
```

## 🐛 Troubleshooting Test Issues

### Service Not Responding

**Symptom:**
```json
{
  "error": "Service unavailable",
  "message": "Could not connect to the target service"
}
```

**Solution:**
1. Check if all services are running: `curl http://localhost:8080/health`
2. Verify logs in the terminal
3. Restart the system: Press CTRL+C and run `python run_system.py` again

### Port Conflicts

**Symptom:**
```
✗ Error: The following ports are already in use:
  • Port 5000 - Main Flask Server
```

**Solution:**
```bash
# Windows
netstat -ano | findstr :5000
taskkill /PID <PID> /F

# Or just restart your computer
```

### Gateway Returns 404

**Symptom:**
```json
{
  "error": "Route not found",
  "message": "Gateway does not have a route for /api/wrong/path",
  "available_routes": [...]
}
```

**Solution:**
Check your URL path. Valid routes are:
- `/api/main/*`
- `/api/ai/chat`
- `/api/ai/assessment`

## 📊 Performance Testing

### Load Testing with Apache Bench

```bash
# Install Apache Bench (comes with Apache HTTP Server)

# Test gateway performance
ab -n 1000 -c 10 http://localhost:8080/health

# Test through gateway to main server
ab -n 100 -c 5 http://localhost:8080/api/main/health
```

### Expected Metrics

- **Gateway Overhead:** 5-15ms per request
- **Total Response Time:** Service time + Gateway overhead
- **Concurrent Connections:** Gateway handles 100+ concurrent connections

## ✅ Success Checklist

- [ ] All 4 services start without errors
- [ ] Gateway health check returns all services as "online"
- [ ] Can access main server through gateway
- [ ] Chatbot responds correctly through gateway
- [ ] Stroke assessment works through gateway
- [ ] Gateway logs show all requests
- [ ] CTRL+C stops all services gracefully
- [ ] Can restart system without port conflicts

---

**Happy Testing! 🚀**

If you encounter issues, check the `ORCHESTRATION_GUIDE.md` for more detailed troubleshooting steps.
