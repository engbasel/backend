# NeuroAid Backend - Quick Start Guide

## 🚀 Quick Setup (5 Minutes)

### Prerequisites
- Node.js 16+ installed
- Python 3.8+ installed
- Git (optional)

---

## Step 1: Install Backend Dependencies

Open terminal in the `backend` directory:

```bash
npm install
```

---

## Step 2: Install AI Services Dependencies

Open terminal in the `backend/ai_services` directory:

```bash
# On Windows
install_dependencies.bat

# Or manually for each service:
cd chatbot && pip install -r requirements.txt && cd ..
cd stroke_assessment && pip install -r requirements.txt && cd ..
cd stroke_image && pip install -r requirements.txt && cd ..
```

---

## Step 3: Configure Environment

The `.env` file is already configured with default values. You can modify it if needed:

```env
PORT=3001
NODE_ENV=development

# AI Services URLs (default)
AI_CHATBOT_URL=http://localhost:5001
AI_STROKE_QA_URL=http://localhost:5002
AI_STROKE_IMAGE_URL=http://localhost:5003

# JWT Configuration
JWT_SECRET=your-secret-key-change-this-in-production
JWT_EXPIRES_IN=7d
```

---

## Step 4: Start All Services

### Option A: Automated (Recommended)

**Terminal 1 - Start Backend:**
```bash
npm start
```

**Terminal 2 - Start AI Services:**
```bash
cd ai_services
start_all_services.bat
```

### Option B: Manual Start

**Terminal 1 - Backend:**
```bash
npm start
```

**Terminal 2 - Chatbot:**
```bash
cd ai_services/chatbot
python app.py
```

**Terminal 3 - Stroke Assessment:**
```bash
cd ai_services/stroke_assessment
python app.py
```

**Terminal 4 - Image Analysis:**
```bash
cd ai_services/stroke_image
python app.py
```

---

## Step 5: Verify Everything is Running

Open your browser and check these URLs:

### Backend
- **Main Backend**: http://localhost:3001/health
- **Config**: http://localhost:3001/config

### AI Services
- **Chatbot**: http://localhost:5001/health
- **Stroke Assessment**: http://localhost:5002/health
- **Image Analysis**: http://localhost:5003/health

You should see "OK" status for all services.

---

## Step 6: Test the APIs

### Using the Test Script

```bash
node test_api.js
```

This will test all major endpoints and show you the results.

### Manual Testing with cURL

**Register a User:**
```bash
curl -X POST http://localhost:3001/api/auth/register ^
  -H "Content-Type: application/json" ^
  -d "{\"name\":\"Test User\",\"email\":\"test@example.com\",\"password\":\"password123\",\"phone\":\"01234567890\"}"
```

**Login:**
```bash
curl -X POST http://localhost:3001/api/auth/login ^
  -H "Content-Type: application/json" ^
  -d "{\"email\":\"test@example.com\",\"password\":\"password123\"}"
```

Copy the token from the response and use it in the next requests.

**Test Chatbot:**
```bash
curl -X POST http://localhost:3001/api/ai/chat ^
  -H "Content-Type: application/json" ^
  -H "Authorization: Bearer YOUR_TOKEN_HERE" ^
  -d "{\"message\":\"ما هي أعراض السكتة الدماغية؟\"}"
```

**Test Stroke Assessment:**
```bash
curl -X POST http://localhost:3001/api/ai/stroke-assessment ^
  -H "Content-Type: application/json" ^
  -H "Authorization: Bearer YOUR_TOKEN_HERE" ^
  -d "{\"age\":65,\"gender\":\"Male\",\"hypertension\":1,\"heartDisease\":0,\"avgGlucoseLevel\":120,\"bmi\":28,\"smokingStatus\":\"formerly smoked\"}"
```

---

## Step 7: Connect Your Flutter App

### Update API Configuration

In your Flutter app, the API service should already be configured to use:

```dart
// For Android Emulator
http://10.0.2.2:3001

// For Physical Device (same network)
http://YOUR_COMPUTER_IP:3001
```

### Find Your Computer's IP

**Windows:**
```bash
ipconfig
```
Look for "IPv4 Address" under your active network adapter.

**The backend automatically updates** `backend/config.json` with your IP when you run `npm start`.

---

## 📱 Mobile App Integration

### Android Emulator
The app is already configured to use `http://10.0.2.2:3001`

### Physical Device
1. Make sure your phone and computer are on the same WiFi network
2. Find your computer's IP address (e.g., 192.168.1.27)
3. The app will automatically fetch the correct IP from `http://10.0.2.2:3001/config`

---

## 🎯 Available Features

### 1. AI Chatbot
- Ask questions about stroke in Arabic
- Get instant responses
- Conversation history support

### 2. Stroke Risk Assessment
- Input patient data
- Get risk percentage and level
- Receive personalized recommendations in Arabic

### 3. Brain Scan Analysis
- Upload brain scan images
- Get AI analysis results
- View confidence scores and findings

### 4. Doctor Booking
- Browse available doctors
- Book appointments
- Manage bookings

### 5. User Management
- Register and login
- Profile management
- Secure authentication with JWT

---

## 🔧 Troubleshooting

### Backend won't start
- Check if port 3001 is already in use
- Run: `netstat -ano | findstr :3001`
- Kill the process or change the port in `.env`

### AI Services won't start
- Check if Python is installed: `python --version`
- Check if ports 5001-5003 are available
- Install dependencies again: `pip install -r requirements.txt`

### Can't connect from mobile app
- Check firewall settings (allow ports 3001, 5001-5003)
- Verify both devices are on same network
- Check the IP address in config.json

### CORS errors
- CORS is already enabled in the backend
- If issues persist, check the CORS configuration in `server.js`

### AI Services return mock data
- This is normal if AI models are not loaded
- The services work with rule-based logic as fallback
- To use ML models, place trained models in respective directories

---

## 📊 Project Structure

```
backend/
├── server.js              # Main Express server
├── package.json           # Node.js dependencies
├── .env                   # Environment configuration
├── routes/                # API routes
│   ├── auth.js           # Authentication
│   ├── ai.js             # AI endpoints (proxy to Python services)
│   ├── doctors.js        # Doctors management
│   ├── bookings.js       # Appointments
│   └── ...
├── middleware/           # Custom middleware
│   └── auth.js          # JWT authentication
├── data/                # Database (JSON files)
│   └── db.json         # Main database
├── uploads/            # Uploaded files
│   └── scans/         # Brain scan images
└── ai_services/       # Python AI microservices
    ├── chatbot/       # AI Chatbot service
    ├── stroke_assessment/  # Risk assessment
    └── stroke_image/  # Image analysis
```

---

## 🎓 Next Steps

1. **Read the API Documentation**: `API_DOCUMENTATION.md`
2. **Explore AI Services**: `ai_services/README.md`
3. **Customize responses**: Edit Python files in `ai_services/`
4. **Add ML models**: Place trained models in service directories
5. **Deploy to production**: See deployment guides

---

## 📞 Support

For issues or questions:
1. Check the troubleshooting section above
2. Review the API documentation
3. Check the AI services README
4. Contact the development team

---

## 🔐 Security Notes

**For Development:**
- Default JWT secret is used (change in production)
- No HTTPS (use HTTPS in production)
- CORS is wide open (restrict in production)

**For Production:**
- Change JWT_SECRET in `.env`
- Use HTTPS
- Configure CORS properly
- Use environment variables for sensitive data
- Set up proper database (PostgreSQL, MongoDB)
- Enable rate limiting
- Add logging and monitoring

---

## ✅ Checklist

- [ ] Node.js installed
- [ ] Python installed
- [ ] Backend dependencies installed (`npm install`)
- [ ] AI services dependencies installed
- [ ] Backend running on port 3001
- [ ] All AI services running (5001-5003)
- [ ] Health checks passing
- [ ] Test API script runs successfully
- [ ] Mobile app can connect

---

**You're all set! 🎉**

The backend is now ready to use with your Flutter app. All 3 AI features are integrated and working!
