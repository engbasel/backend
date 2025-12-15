# NeuroAid LAN - Quick Start Guide

## 🚀 **5-Minute Setup**

### **Step 1: Configure Firewall (One-Time Setup)**
```batch
cd backend
configure_firewall.bat
```
Right-click → **Run as Administrator**

---

### **Step 2: Start Backend**
```batch
cd backend
start_lan_backend.bat
```

**Copy the IP address shown**, for example:
```
Local IP Address: 192.168.1.100
```

---

### **Step 3: Update Flutter App**

**File:** `lib/src/core/constants/api_constants.dart`

**Line 28 - Change this:**
```dart
static const String _networkIp = '192.168.1.6';  // ← OLD IP
```

**To this (use YOUR IP from Step 2):**
```dart
static const String _networkIp = '192.168.1.100';  // ← YOUR IP
```

**Save the file.**

---

### **Step 4: Test from Mobile Browser**

Open mobile browser, visit:
```
http://192.168.1.100:8080/health
```
(Replace with YOUR IP)

**Should see:**
```json
{"gateway": "OK", "services": {...}}
```

---

### **Step 5: Run Flutter App**
```batch
flutter run
```

**Done!** App should connect successfully.

---

## ⚡ **Quick Commands**

### **Get Your IP:**
```batch
ipconfig | findstr IPv4
```

### **Test Health Endpoint:**
```batch
curl http://localhost:8080/health
```

### **Check Firewall:**
```batch
netsh advfirewall firewall show rule name="NeuroAid Gateway"
```

### **Kill Port 8080:**
```batch
netstat -ano | findstr :8080
taskkill /PID <process_id> /F
```

---

## 🐛 **Quick Troubleshooting**

### **Can't Connect?**
1. ✅ Backend running? (Check terminal)
2. ✅ Same WiFi? (Check both devices)
3. ✅ Correct IP in Flutter app?
4. ✅ Firewall configured? (Run `configure_firewall.bat` as Admin)
5. ✅ Network is Private? (Not Public)

### **Test from laptop browser first:**
```
http://localhost:8080/health  ← Should work
http://192.168.1.100:8080/health  ← Should work
```

### **Then test from mobile browser:**
```
http://192.168.1.100:8080/health  ← Should work
```

---

## 📱 **Mobile Testing**

### **From Browser:**
```
http://YOUR_IP:8080/health
```

### **From Flutter App:**
- Login
- View profile
- Use AI Chat
- Run stroke assessment

---

## 📋 **Pre-Launch Checklist**

- [ ] Firewall configured (one-time setup)
- [ ] Backend started (`start_lan_backend.bat`)
- [ ] IP address noted
- [ ] Flutter app updated with correct IP
- [ ] Both devices on same WiFi
- [ ] Network set to "Private"
- [ ] Health endpoint tested from mobile browser

---

## 📚 **Full Documentation**

- **Complete Guide:** `LAN_SETUP_GUIDE.md`
- **All Changes:** `LAN_FIX_SUMMARY.md`
- **API Docs:** `API_DOCUMENTATION.md`

---

## 🎯 **Expected Results**

### **Terminal Output:**
```
============================================================
                  NeuroAid LAN Backend Startup
============================================================

Local IP Address: 192.168.1.100
Gateway Port: 8080

📱 LAN Access URLs (use on mobile devices):
   Gateway: http://192.168.1.100:8080
   Health:  http://192.168.1.100:8080/health
```

### **Mobile Browser:**
```json
{
  "gateway": "OK",
  "timestamp": "2025-12-13T14:30:00.000Z",
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

### **Flutter App:**
- ✅ Connects successfully
- ✅ Login works
- ✅ Data loads
- ✅ AI features work
- ✅ No "internet connection" errors

---

**Last Updated:** December 13, 2025
