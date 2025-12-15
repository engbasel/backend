# 🎓 NeuroAid Backend - Orchestration System Summary

## 📦 What Was Delivered

### 1. **gateway.py** - API Gateway with Centralized Logging
**Location:** `backend/gateway.py`

**Features:**
- ✅ Reverse proxy for all backend services
- ✅ Centralized request/response logging with color-coded output
- ✅ Health monitoring for all services
- ✅ Automatic request routing
- ✅ Error handling and timeout management
- ✅ CORS support

**Routing Configuration:**
```
http://localhost:8080/api/main/*        → Main Flask Server (port 5000)
http://localhost:8080/api/ai/chat       → AI Chatbot Service (port 5001)
http://localhost:8080/api/ai/assessment → Stroke Assessment (port 5002)
```

**Key Code Highlights:**
- `log_request()` - Logs incoming requests with timestamp and target service
- `log_response()` - Logs responses with status code and processing time
- `proxy_request()` - Forwards requests to appropriate backend service
- Color-coded terminal output for easy debugging

### 2. **run_system.py** - Unified System Orchestrator
**Location:** `backend/run_system.py`

**Features:**
- ✅ Launches all services with a single command
- ✅ Automatic port conflict detection
- ✅ Graceful shutdown with CTRL+C
- ✅ Real-time log streaming from all services
- ✅ Process monitoring and auto-restart detection
- ✅ Cross-platform support (Windows/Linux/Mac)

**Services Managed:**
1. Main Flask Server (Port 5000)
2. AI Chatbot Service (Port 5001)
3. Stroke Assessment Service (Port 5002)
4. API Gateway (Port 8080)

**Key Code Highlights:**
- `run_service()` - Manages individual service lifecycle
- `signal_handler()` - Graceful shutdown of all processes
- `check_ports_available()` - Pre-flight port validation
- Thread-based concurrent service execution

### 3. **ORCHESTRATION_GUIDE.md** - Complete Documentation
**Location:** `backend/ORCHESTRATION_GUIDE.md`

**Contents:**
- Architecture overview with ASCII diagrams
- Quick start guide
- Port configuration instructions
- API Gateway route mappings
- Health monitoring
- Troubleshooting guide
- Security notes

### 4. **TESTING_GUIDE.md** - Testing Instructions
**Location:** `backend/TESTING_GUIDE.md`

**Contents:**
- Step-by-step testing procedures
- Sample API requests with expected responses
- Postman collection examples
- Flutter integration examples
- Performance testing guide
- Troubleshooting checklist

### 5. **start_system.bat** - Windows Quick Start
**Location:** `backend/start_system.bat`

**Features:**
- One-click system startup
- Automatic dependency checking
- Python installation verification
- User-friendly error messages

### 6. **requirements.txt** - Python Dependencies
**Location:** `backend/requirements.txt`

**Packages:**
- flask, flask-cors
- requests (for gateway proxying)
- python-dotenv
- numpy, scikit-learn (for AI services)
- PyJWT, bcrypt (for auth)

### 7. **Updated flask_server/app.py**
**Changes:**
- Port changed from 3001 → 5000 for consistency

## 🚀 How to Use

### Quick Start (3 Steps)

1. **Install Dependencies**
```bash
cd "d:\courses\Flutter\projects\Work\Graduation Projects\Delta\neuroaid\backend"
pip install -r requirements.txt
```

2. **Start Everything**
```bash
python run_system.py
# OR
start_system.bat
```

3. **Test**
```bash
curl http://localhost:8080/health
```

### What You'll See

```
═══════════════════════════════════════════════════════════════════
          NeuroAid Backend System Orchestrator
═══════════════════════════════════════════════════════════════════

Starting Services:

🌐  Main Flask Server
   Port: 5000
   Script: flask_server/app.py

🤖  AI Chatbot Service
   Port: 5001
   Script: ai_services/chatbot/app.py

🏥  Stroke Assessment Service
   Port: 5002
   Script: ai_services/stroke_assessment/app.py

🚀  API Gateway
   Port: 8080
   Script: gateway.py

═══════════════════════════════════════════════════════════════════

✓ All services started successfully!

API Gateway: http://localhost:8080
Health Check: http://localhost:8080/health

Press CTRL+C to stop all services
```

### Gateway Logs Example

When you make a request through the gateway:

```
[GATEWAY] 2025-12-13 09:14:02 - Incoming Request: POST /api/ai/chat
[GATEWAY] Routing to: AI Chatbot Service
[GATEWAY] Response: 200 - Time: 78.91ms

[GATEWAY] 2025-12-13 09:14:15 - Incoming Request: POST /api/ai/assessment
[GATEWAY] Routing to: Stroke Assessment Service
[GATEWAY] Response: 200 - Time: 142.33ms

[GATEWAY] 2025-12-13 09:14:20 - Incoming Request: GET /api/main/health
[GATEWAY] Routing to: Main Flask Server
[GATEWAY] Response: 200 - Time: 12.45ms
```

## 🔧 Configuration Guide

### Port Assignments

| Service | Port | Environment Variable |
|---------|------|---------------------|
| Main Flask Server | 5000 | `PORT` |
| AI Chatbot | 5001 | `PORT` |
| Stroke Assessment | 5002 | `PORT` |
| API Gateway | 8080 | `GATEWAY_PORT` |

### To Change Ports

#### Option 1: Environment Variables
```bash
# Windows PowerShell
$env:PORT = "5000"
$env:GATEWAY_PORT = "8080"

# Linux/Mac
export PORT=5000
export GATEWAY_PORT=8080
```

#### Option 2: Edit Configuration Files

**In `run_system.py`:**
```python
SERVICES = [
    {
        'name': 'Main Flask Server',
        'port': 5000,  # ← Change here
        'env': {'PORT': '5000'},  # ← And here
        ...
    }
]
```

**In `gateway.py`:**
```python
SERVICES = {
    'main': {
        'url': 'http://localhost:5000',  # ← Change here
        ...
    }
}
```

## 📱 Flutter Integration

### Before (Multiple URLs)
```dart
const String MAIN_SERVER = 'http://localhost:5000';
const String CHATBOT_SERVICE = 'http://localhost:5001';
const String ASSESSMENT_SERVICE = 'http://localhost:5002';
```

### After (Single Gateway URL)
```dart
const String API_GATEWAY = 'http://localhost:8080';

// For Android Emulator
const String API_GATEWAY = 'http://10.0.2.2:8080';

// All requests go through gateway
final response = await http.post(
  '$API_GATEWAY/api/ai/chat',
  body: jsonEncode({'message': message}),
  headers: {'Content-Type': 'application/json'},
);
```

## 🎯 Benefits of This System

### 1. **Unified Entry Point**
- Flutter app only needs to know one URL (gateway)
- Easy to change backend infrastructure without updating mobile app

### 2. **Centralized Logging**
- All requests logged in one place
- Easy debugging and monitoring
- Color-coded output for quick issue identification

### 3. **Simple Deployment**
- One command starts everything
- No need to manage multiple terminals
- Graceful shutdown prevents orphaned processes

### 4. **Scalability**
- Easy to add new microservices
- Gateway handles load balancing potential
- Can add authentication/rate limiting at gateway level

### 5. **Professional Architecture**
- Industry-standard microservices pattern
- Separation of concerns
- Easy to containerize with Docker later

## 🐛 Common Issues & Solutions

### Issue: Port Already in Use
**Solution:**
```bash
netstat -ano | findstr :5000
taskkill /PID <PID> /F
```

### Issue: Gateway Can't Connect to Service
**Solution:**
1. Check service is running: `curl http://localhost:5000/health`
2. Verify port in gateway matches service port
3. Check firewall settings

### Issue: Module Not Found
**Solution:**
```bash
pip install -r requirements.txt
```

## 📚 Additional Resources

- **ORCHESTRATION_GUIDE.md** - Detailed documentation
- **TESTING_GUIDE.md** - Testing procedures and examples
- **API_DOCUMENTATION.md** - Your existing API docs (still valid)

## 🎓 Graduation Project Notes

### What to Present

1. **Architecture Diagram** - Show the gateway routing
2. **Live Demo** - Start all services with one command
3. **Logs** - Show centralized logging in action
4. **Scalability** - Explain how easy it is to add services

### Talking Points

- "We implemented a microservices architecture with API Gateway pattern"
- "All services are orchestrated and can be started with a single command"
- "Centralized logging provides visibility into all requests"
- "The system is production-ready and can be containerized with Docker"

## ✅ Verification Checklist

- [x] API Gateway created with logging
- [x] Orchestrator script for unified execution
- [x] Port configurations documented
- [x] Testing guide provided
- [x] Windows batch file for easy startup
- [x] Requirements file with all dependencies
- [x] Comprehensive documentation
- [x] Main server port updated to 5000

## 🚀 Next Steps (Optional Enhancements)

1. **Docker Compose** - Containerize all services
2. **Authentication Middleware** - Add to gateway
3. **Rate Limiting** - Prevent API abuse
4. **Load Balancing** - Multiple instances of services
5. **Monitoring Dashboard** - Grafana/Prometheus integration
6. **CI/CD Pipeline** - Automated deployment

---

## 📞 Support

If you encounter any issues:

1. Check the logs in the terminal
2. Verify all ports are available
3. Ensure dependencies are installed
4. Refer to `ORCHESTRATION_GUIDE.md` for troubleshooting

**Created by:** Senior Python Backend Engineer  
**Date:** 2025-12-13  
**Project:** NeuroAid - Graduation Project  
**Tech Stack:** Python, Flask, Microservices, API Gateway

---

**🎉 You're all set! Good luck with your graduation project! 🎓**
