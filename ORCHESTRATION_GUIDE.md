# NeuroAid Backend Orchestration System

## 📋 Overview

This system provides unified execution and centralized API Gateway for all NeuroAid backend services.

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────┐
│         API Gateway (Port 8080)                 │
│  • Centralized Logging                          │
│  • Request Routing                              │
│  • Service Monitoring                           │
└─────────────┬───────────────────────────────────┘
              │
    ┌─────────┴─────────┬─────────────┬──────────┐
    │                   │             │          │
┌───▼────┐      ┌──────▼─────┐  ┌────▼────┐  ┌──▼────┐
│ Main   │      │ AI Chatbot │  │ Stroke  │  │ More  │
│ Flask  │      │  Service   │  │  Risk   │  │  AI   │
│ Server │      │ (Port 5001)│  │ Service │  │ ...   │
│(Port   │      └────────────┘  │(Port    │  └───────┘
│ 5000)  │                      │ 5002)   │
└────────┘                      └─────────┘
```

## 📁 Project Structure

```
backend/
├── flask_server/          # Main Flask application (Port 5000)
│   ├── app.py
│   ├── routes/
│   ├── utils/
│   └── ...
├── ai_services/           # AI microservices
│   ├── chatbot/           # Chatbot service (Port 5001)
│   │   └── app.py
│   ├── stroke_assessment/ # Assessment service (Port 5002)
│   │   └── app.py
│   └── ...
├── gateway.py             # API Gateway (Port 8080) 🆕
├── run_system.py          # System orchestrator 🆕
└── ORCHESTRATION_GUIDE.md # This file
```

## 🚀 Quick Start

### Prerequisites

Install the `requests` library for the gateway:

```bash
pip install requests flask flask-cors
```

### Running the Entire System

From the `backend` directory, run:

```bash
python run_system.py
```

This will start:
- ✅ Main Flask Server (Port 5000)
- ✅ AI Chatbot Service (Port 5001)
- ✅ Stroke Assessment Service (Port 5002)
- ✅ API Gateway (Port 8080)

### Stopping the System

Press **CTRL+C** in the terminal. All services will shut down gracefully.

## 🔧 Port Configuration

### Current Port Assignments

| Service | Port | Status |
|---------|------|--------|
| **API Gateway** | 8080 | 🆕 Main entry point |
| Main Flask Server | 5000 | ✅ Active |
| AI Chatbot | 5001 | ✅ Active |
| Stroke Assessment | 5002 | ✅ Active |

### How to Change Ports

#### 1. Main Flask Server (flask_server/app.py)

**Current configuration (line 138):**
```python
port = int(os.getenv('PORT', 3001))
```

**Change to:**
```python
port = int(os.getenv('PORT', 5000))
```

Or set environment variable:
```bash
# Windows (PowerShell)
$env:PORT = "5000"

# Windows (CMD)
set PORT=5000

# Linux/Mac
export PORT=5000
```

#### 2. AI Chatbot Service (ai_services/chatbot/app.py)

**Current configuration (line 102):**
```python
port = int(os.environ.get('PORT', 5001))
```

This is already set correctly. To change:
```python
port = int(os.environ.get('PORT', YOUR_NEW_PORT))
```

#### 3. Stroke Assessment Service (ai_services/stroke_assessment/app.py)

**Current configuration (line 207):**
```python
port = int(os.environ.get('PORT', 5002))
```

This is already set correctly. To change:
```python
port = int(os.environ.get('PORT', YOUR_NEW_PORT))
```

#### 4. API Gateway (gateway.py)

**Current configuration (line 306):**
```python
GATEWAY_PORT = int(os.environ.get('GATEWAY_PORT', 8080))
```

To change:
```python
GATEWAY_PORT = int(os.environ.get('GATEWAY_PORT', YOUR_NEW_PORT))
```

#### 5. Update Orchestrator (run_system.py)

If you change ports, update the `SERVICES` configuration in `run_system.py`:

```python
SERVICES = [
    {
        'name': 'Main Flask Server',
        'port': 5000,  # ← Update this
        'script': 'flask_server/app.py',
        'env': {'PORT': '5000'},  # ← And this
        'emoji': '🌐'
    },
    # ... update other services similarly
]
```

## 🌐 API Gateway Routes

### Gateway Endpoints

| Client Request | Routes To | Target Service |
|---------------|-----------|----------------|
| `GET /health` | Gateway Health | API Gateway |
| `POST /api/main/*` | `http://localhost:5000/api/*` | Main Flask Server |
| `POST /api/ai/chat` | `http://localhost:5001/chat` | AI Chatbot |
| `POST /api/ai/assessment` | `http://localhost:5002/predict` | Stroke Assessment |

### Example Usage

**Before (Direct to services):**
```javascript
// Flutter/Mobile app had to know all service URLs
fetch('http://localhost:5000/api/auth/login', { ... })
fetch('http://localhost:5001/chat', { ... })
fetch('http://localhost:5002/predict', { ... })
```

**After (Through Gateway):**
```javascript
// Single entry point
const GATEWAY_URL = 'http://localhost:8080';

// All requests go through gateway
fetch(`${GATEWAY_URL}/api/main/auth/login`, { ... })
fetch(`${GATEWAY_URL}/api/ai/chat`, { ... })
fetch(`${GATEWAY_URL}/api/ai/assessment`, { ... })
```

## 📊 Centralized Logging

The gateway provides detailed logging for every request:

```
[GATEWAY] 2025-12-13 09:14:02 - Incoming Request: POST /api/ai/chat
[GATEWAY] Routing to: AI Chatbot Service
[GATEWAY] Response: 200 - Time: 245.67ms
```

**Log Features:**
- ✅ Request method and path
- ✅ Target service name
- ✅ Response status code
- ✅ Request processing time
- ✅ Color-coded output for easy reading

## 🔍 Health Monitoring

### Check All Services

```bash
curl http://localhost:8080/health
```

**Response:**
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

### Check Individual Services

```bash
# Main server
curl http://localhost:5000/health

# Chatbot
curl http://localhost:5001/health

# Assessment
curl http://localhost:5002/health
```

## 🛠️ Troubleshooting

### Port Already in Use

**Error:**
```
✗ Error: The following ports are already in use:
  • Port 5000 - Main Flask Server
```

**Solution:**
```bash
# Windows - Find and kill process using port
netstat -ano | findstr :5000
taskkill /PID <PID> /F

# Linux/Mac
lsof -ti:5000 | xargs kill -9
```

### Service Won't Start

**Check:**
1. Are you in the `backend` directory?
2. Do you have all dependencies installed?
3. Are environment variables set correctly?

**Solution:**
```bash
# Verify directory
pwd  # Should show: .../neuroaid/backend

# Install dependencies
pip install -r requirements.txt  # If you have one
pip install flask flask-cors requests python-dotenv
```

### Gateway Can't Connect to Service

**Check logs for:**
```
Service unavailable - Could not connect to the target service
```

**Solution:**
1. Ensure the target service is running
2. Check if the port in `gateway.py` SERVICES config matches the actual service port
3. Verify firewall settings aren't blocking connections

## 📝 Running Services Individually

### For Development/Testing

Instead of running all services, you can run them individually:

```bash
# Terminal 1 - Main server
cd flask_server
python app.py

# Terminal 2 - Chatbot
cd ai_services/chatbot
python app.py

# Terminal 3 - Assessment
cd ai_services/stroke_assessment
python app.py

# Terminal 4 - Gateway
cd backend
python gateway.py
```

## 🔐 Security Notes

1. **CORS:** The gateway has CORS enabled. Configure it properly for production.
2. **Authentication:** Add authentication middleware to the gateway if needed.
3. **Rate Limiting:** Consider adding rate limiting to the gateway.
4. **HTTPS:** Use a reverse proxy (nginx) with SSL certificates in production.

## 📦 Dependencies

Add to your `requirements.txt`:

```txt
flask>=2.3.0
flask-cors>=4.0.0
requests>=2.31.0
python-dotenv>=1.0.0
```

Install:
```bash
pip install -r requirements.txt
```

## 🎯 Next Steps

1. **Update Mobile App:** Point all API calls to `http://localhost:8080` instead of individual service URLs
2. **Add More Services:** Add new microservices to `run_system.py` SERVICES list
3. **Environment-Based Config:** Create `.env` file for environment-specific configurations
4. **Docker Support:** Create `docker-compose.yml` for containerized deployment

## 📞 Support

For issues related to:
- **Gateway:** Check `gateway.py` logs
- **Orchestrator:** Check `run_system.py` output
- **Individual Services:** Check service-specific logs

---

**Created by:** Senior Python Backend Engineer  
**Date:** 2025-12-13  
**Project:** NeuroAid Graduation Project
