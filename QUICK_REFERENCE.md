# 🚀 NeuroAid Backend - Quick Reference Card

## ⚡ Quick Commands

### Start System
```bash
# Option 1: Python (Cross-platform)
python run_system.py

# Option 2: Batch File (Windows)
start_system.bat
```

### Stop System
```
Press CTRL+C in the terminal
```

### Install Dependencies
```bash
pip install -r requirements.txt
```

## 🌐 Essential URLs

| Service | URL | Description |
|---------|-----|-------------|
| **API Gateway** | http://localhost:8080 | ⭐ Main entry point |
| Gateway Health | http://localhost:8080/health | Check all services |
| Main Flask Server | http://localhost:5000 | Direct access (dev only) |
| AI Chatbot | http://localhost:5001 | Direct access (dev only) |
| Stroke Assessment | http://localhost:5002 | Direct access (dev only) |

## 📍 API Routes (Through Gateway)

### Main Server Routes
```
http://localhost:8080/api/main/health
http://localhost:8080/api/main/auth/login
http://localhost:8080/api/main/auth/register
http://localhost:8080/api/main/users
http://localhost:8080/api/main/doctors
http://localhost:8080/api/main/bookings
http://localhost:8080/api/main/scans
```

### AI Service Routes
```
POST http://localhost:8080/api/ai/chat
POST http://localhost:8080/api/ai/assessment
```

## 🧪 Quick Tests

### Test 1: Gateway Health
```bash
curl http://localhost:8080/health
```

### Test 2: Chatbot
```bash
curl -X POST http://localhost:8080/api/ai/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "مرحبا"}'
```

### Test 3: Stroke Assessment
```bash
curl -X POST http://localhost:8080/api/ai/assessment \
  -H "Content-Type: application/json" \
  -d '{"age": 55, "gender": "Male", "hypertension": 0, "heart_disease": 0, "avg_glucose_level": 100, "bmi": 25, "smoking_status": "never smoked"}'
```

## 📁 Key Files

| File | Purpose | When to Use |
|------|---------|-------------|
| `gateway.py` | API Gateway | Don't modify unless adding routes |
| `run_system.py` | Orchestrator | Modify to add new services |
| `start_system.bat` | Quick start | Run to start everything |
| `requirements.txt` | Dependencies | Run when missing packages |
| `SYSTEM_SUMMARY.md` | Full docs | Read for complete understanding |
| `TESTING_GUIDE.md` | Testing | Use for testing procedures |

## 🎨 Gateway Logging

When you make a request, you'll see:
```
[GATEWAY] 2025-12-13 09:14:02 - Incoming Request: POST /api/ai/chat
[GATEWAY] Routing to: AI Chatbot Service
[GATEWAY] Response: 200 - Time: 78.91ms
```

**Colors:**
- 🟦 Cyan = Incoming request
- 🟩 Green = Service name & success
- 🟨 Yellow = Response time
- 🟥 Red = Errors

## 🔧 Common Fixes

### "Port already in use"
```bash
# Windows
netstat -ano | findstr :8080
taskkill /PID <PID> /F

# Or restart computer
```

### "Service unavailable"
```bash
# Check if service is running
curl http://localhost:8080/health

# Restart system
# CTRL+C, then: python run_system.py
```

### "Module not found"
```bash
pip install -r requirements.txt
```

## 📱 Flutter Integration

### Update API Base URL
```dart
// Change from multiple URLs
const String MAIN_SERVER = 'http://localhost:5000';
const String CHATBOT_SERVICE = 'http://localhost:5001';

// To single gateway URL
const String API_GATEWAY = 'http://localhost:8080';

// For Android Emulator
const String API_GATEWAY = 'http://10.0.2.2:8080';
```

### Update API Calls
```dart
// Old way
await http.post('http://localhost:5001/chat', ...);

// New way (through gateway)
await http.post('http://localhost:8080/api/ai/chat', ...);
```

## 🎯 Port Quick Reference

```
5000 → Main Flask Server
5001 → AI Chatbot
5002 → Stroke Assessment
8080 → API Gateway ⭐ USE THIS
```

## 📋 Startup Checklist

- [ ] In `backend` directory?
- [ ] Dependencies installed? (`pip install -r requirements.txt`)
- [ ] Ports available? (nothing else using 5000, 5001, 5002, 8080)
- [ ] Run: `python run_system.py`
- [ ] Test: `curl http://localhost:8080/health`
- [ ] All services show "online"? ✅

## 🎓 For Your Presentation

### Demo Script
1. Show `python run_system.py` - all services start
2. Open browser: `http://localhost:8080/health`
3. Test chatbot: Postman/curl
4. Show gateway logs in terminal
5. Press CTRL+C - graceful shutdown

### Key Points to Mention
✅ Microservices architecture  
✅ API Gateway pattern  
✅ Centralized logging  
✅ One-command deployment  
✅ Production-ready design  

## 📞 Getting Help

1. Check **SYSTEM_SUMMARY.md** for overview
2. Check **ORCHESTRATION_GUIDE.md** for details
3. Check **TESTING_GUIDE.md** for testing
4. Check terminal logs for errors

---

**💡 Pro Tip:** Bookmark this file for quick reference during development!

**🎉 Happy Coding!**
