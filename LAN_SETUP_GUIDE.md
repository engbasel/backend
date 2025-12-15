# NeuroAid LAN Setup Guide

## Complete Guide for Running Backend on Local Network

This guide will help you set up the NeuroAid backend to be accessible from any device on your local network (same WiFi) **without requiring internet access**.

---

## 🎯 **Quick Start Checklist**

- [ ] Configure Windows Firewall
- [ ] Find your laptop's local IP address
- [ ] Update Flutter app configuration
- [ ] Start backend services
- [ ] Test from mobile device

---

## 📋 **Step-by-Step Setup**

### **Step 1: Configure Windows Firewall**

**Run as Administrator:**

```batch
cd backend
configure_firewall.bat
```

Right-click → "Run as Administrator"

**What it does:**
- Opens ports: 8080 (Gateway), 5000 (Flask), 5001 (Chatbot), 5002 (Assessment), 5003 (Image)
- Configures firewall for Private networks only

**Verification:**
```batch
netsh advfirewall firewall show rule name="NeuroAid Gateway"
```

---

### **Step 2: Find Your Laptop's IP Address**

**Windows (Command Prompt):**
```batch
ipconfig
```

**Look for:**
```
Wireless LAN adapter Wi-Fi:
   IPv4 Address. . . . . . . . . . . : 192.168.1.100
```

**Note this IP address** - you'll need it for Step 3.

**Common IP ranges:**
- `192.168.1.x` (most home routers)
- `192.168.0.x` (some home routers)
- `10.0.0.x` (some office networks)

---

### **Step 3: Update Flutter App Configuration**

**File:** `lib/src/core/constants/api_constants.dart`

**Find this line (around line 28):**
```dart
static const String _networkIp = '192.168.1.6';
```

**Replace with YOUR IP from Step 2:**
```dart
static const String _networkIp = '192.168.1.100';  // ← Use YOUR IP here
```

**Save the file.**

---

### **Step 4: Start Backend Services**

**Option A: Start All Services (Recommended)**
```batch
cd backend
python gateway.py
```

**Option B: Start with Batch Script**
```batch
cd backend
start_system.bat
```

**You should see:**
```
============================================================
🚀 NeuroAid API Gateway Started
============================================================

📱 LAN Access URLs (use on mobile devices):
   Gateway: http://192.168.1.100:8080
   Health:  http://192.168.1.100:8080/health

💻 Localhost URLs (for this computer):
   Gateway: http://localhost:8080
   Health:  http://localhost:8080/health

Service Routes:
  ✓ /api/main/*        → Main Flask Server (port 5000)
  ✓ /api/ai/chat       → AI Chatbot Service (port 5001)
  ✓ /api/ai/assessment → Stroke Assessment Service (port 5002)

🔧 Configuration for Flutter App:
   Update api_constants.dart:
   static const String _networkIp = '192.168.1.100';

============================================================
```

**⚠️ IMPORTANT:** Copy the IP address shown under "LAN Access URLs"

---

### **Step 5: Test from Mobile Device**

#### **5.1 Ensure Same WiFi Network**
- Laptop and mobile device **MUST** be on the same WiFi network
- Check WiFi name on both devices

#### **5.2 Test Backend Accessibility**

**From mobile device browser, visit:**
```
http://192.168.1.100:8080/health
```
(Replace with YOUR IP)

**Expected Response:**
```json
{
  "gateway": "OK",
  "timestamp": "2025-12-13T...",
  "services": {
    "main": {
      "status": "online",
      "url": "http://127.0.0.1:5000"
    },
    "ai_chatbot": {
      "status": "online",
      "url": "http://127.0.0.1:5001"
    },
    "ai_assessment": {
      "status": "online",
      "url": "http://127.0.0.1:5002"
    }
  }
}
```

#### **5.3 Run Flutter App**

**From your development machine:**
```batch
flutter run
```

Or deploy to your phone and run.

**The app should now connect successfully!**

---

## 🔍 **Troubleshooting**

### **Problem: "Cannot connect to server"**

**Checklist:**
1. ✅ Backend is running (check terminal window)
2. ✅ Both devices on same WiFi
3. ✅ IP address in `api_constants.dart` is correct
4. ✅ Firewall rules configured (run `configure_firewall.bat` as admin)
5. ✅ Network is set to "Private" (not "Public")

**Test backend from laptop first:**
```
http://localhost:8080/health
```

**Then test from mobile browser:**
```
http://YOUR_IP:8080/health
```

---

### **Problem: Firewall blocking connections**

**Check firewall rules:**
```batch
netsh advfirewall firewall show rule name="NeuroAid Gateway"
```

**Reset firewall rules:**
```batch
configure_firewall.bat
```
(Run as Administrator)

---

### **Problem: Wrong IP address**

**Your IP might change if:**
- Router restarted
- Reconnected to WiFi
- DHCP lease expired

**Solution:**
1. Run `ipconfig` again
2. Update `api_constants.dart` with new IP
3. Restart Flutter app

---

### **Problem: Services not starting**

**Check if ports are already in use:**
```batch
netstat -ano | findstr :8080
netstat -ano | findstr :5000
netstat -ano | findstr :5001
netstat -ano | findstr :5002
```

**Kill process if needed:**
```batch
taskkill /PID <process_id> /F
```

---

## 🧪 **Testing Endpoints**

### **Test URLs (replace IP with yours)**

#### **Gateway Health Check**
```
GET http://192.168.1.100:8080/health
```

#### **Main Server Health**
```
GET http://192.168.1.100:8080/api/main/health
```

#### **AI Chatbot**
```
POST http://192.168.1.100:8080/api/ai/chat
Content-Type: application/json

{
  "message": "Hello",
  "history": []
}
```

#### **Stroke Assessment**
```
POST http://192.168.1.100:8080/api/ai/assessment
Content-Type: application/json

{
  "age": 45,
  "gender": "Male",
  "hypertension": 0,
  "heart_disease": 0,
  "avg_glucose_level": 100,
  "bmi": 25,
  "smoking_status": "never smoked"
}
```

---

## 📱 **Mobile Testing Tools**

### **Recommended Apps:**

1. **Postman** (API testing)
2. **HTTP Request** (Simple HTTP testing)
3. **Your mobile browser** (For health checks)

### **Using Browser:**
Simply open your mobile browser and visit:
```
http://192.168.1.100:8080/health
```

---

## 🔒 **Security Notes**

### **Current Configuration:**
- ✅ Firewall allows only **Private network** access
- ✅ CORS configured for all origins (local network only)
- ✅ Server binds to `0.0.0.0` (all network interfaces)

### **For Production:**
1. Replace `CORS(app, resources={r"/*": {"origins": "*"}})` with specific origins
2. Add authentication tokens
3. Use HTTPS with SSL certificates
4. Restrict firewall to specific IP ranges

---

## 📊 **Architecture Overview**

```
Mobile Device (192.168.1.50)
     |
     | WiFi (same network)
     |
     ↓
Gateway :8080 (192.168.1.100)
     |
     ├→ Flask Server :5000 (127.0.0.1)
     ├→ AI Chatbot :5001 (127.0.0.1)
     ├→ Stroke Assessment :5002 (127.0.0.1)
     └→ Image Analysis :5003 (127.0.0.1)
```

**Key Points:**
- Mobile device connects to Gateway via LAN IP
- Gateway proxies requests to local services on 127.0.0.1
- All services run on the same laptop
- No internet required after setup

---

## 🎓 **Best Practices**

### **1. Static IP (Optional but Recommended)**

**Set static IP on your laptop:**
- Windows Settings → Network → WiFi → Properties
- IP assignment: Manual
- Set IP, Subnet, Gateway

**Benefits:**
- IP doesn't change
- No need to update Flutter app constantly

### **2. Run Backend on Startup (Optional)**

Create shortcut to `start_system.bat`:
- Right-click → Properties
- Target: `"C:\path\to\backend\start_system.bat"`
- Start in: `"C:\path\to\backend"`
- Run: Minimized

### **3. Keep Terminal Open**

- Don't close the terminal window while testing
- Logs show all incoming requests
- Helps with debugging

---

## 📞 **Support Commands**

### **Check if services are running:**
```batch
netstat -ano | findstr :8080
netstat -ano | findstr :5000
```

### **Get your IP quickly:**
```batch
ipconfig | findstr IPv4
```

### **Test from command line:**
```batch
curl http://192.168.1.100:8080/health
```

### **List firewall rules:**
```batch
netsh advfirewall firewall show rule name=all | findstr NeuroAid
```

---

## ✅ **Final Verification Checklist**

Before testing on mobile:

- [ ] Firewall configured (ran `configure_firewall.bat` as admin)
- [ ] Backend running (terminal shows "Gateway Started")
- [ ] IP address noted (from `ipconfig`)
- [ ] Flutter app updated (correct IP in `api_constants.dart`)
- [ ] Same WiFi network (laptop and mobile)
- [ ] Network set to "Private" (Windows settings)
- [ ] Health check works from mobile browser (`http://IP:8080/health`)
- [ ] Flutter app rebuilt after config change

---

## 🎉 **Success Indicators**

### **Backend Terminal:**
```
[GATEWAY] 2025-12-13 14:30:15 - Incoming Request: GET /health
[GATEWAY] Response: 200 - Time: 15.23ms
```

### **Mobile Browser:**
```json
{
  "gateway": "OK",
  "services": { ... }
}
```

### **Flutter App:**
- Login successful
- Data loads
- No "internet connection" errors
- Chat works
- Assessments work

---

## 🔄 **Daily Workflow**

1. Start laptop
2. Connect to WiFi
3. Run `python gateway.py` (or `start_system.bat`)
4. Note IP if changed (usually stays same)
5. Open mobile app
6. Start testing!

---

## 📚 **Additional Resources**

- **Backend Code:** `backend/gateway.py`
- **Flutter Config:** `lib/src/core/constants/api_constants.dart`
- **API Docs:** `backend/API_DOCUMENTATION.md`
- **Error Messages:** Check terminal for detailed logs

---

**Last Updated:** December 13, 2025
**Version:** 1.0
**Author:** NeuroAid Development Team
