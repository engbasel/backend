# Flask Backend - Quick Start (5 دقائق)

## الخطوات

### 1️⃣ التثبيت
```bash
cd flask_server
setup.bat
```

### 2️⃣ التشغيل
```bash
start_server.bat
```

### 3️⃣ التحقق
افتح المتصفح: http://localhost:3001/health

---

## تشغيل النظام الكامل

### الطريقة الأولى: تلقائي (موصى به)

**Terminal 1 - Flask Backend:**
```bash
cd backend\flask_server
start_server.bat
```

**Terminal 2 - AI Services:**
```bash
cd backend\ai_services
start_all_services.bat
```

### الطريقة الثانية: يدوي

**Terminal 1 - Flask Backend:**
```bash
cd backend\flask_server
venv\Scripts\activate
python app.py
```

**Terminal 2 - Chatbot:**
```bash
cd backend\ai_services\chatbot
python app.py
```

**Terminal 3 - Stroke Assessment:**
```bash
cd backend\ai_services\stroke_assessment
python app.py
```

**Terminal 4 - Image Analysis:**
```bash
cd backend\ai_services\stroke_image
python app.py
```

---

## التحقق من الخدمات

افتح هذه الروابط في المتصفح:

- ✅ Flask Backend: http://localhost:3001/health
- ✅ Chatbot: http://localhost:5001/health
- ✅ Assessment: http://localhost:5002/health
- ✅ Image Analysis: http://localhost:5003/health

---

## الاختبار السريع

### 1. Register
```bash
curl -X POST http://localhost:3001/api/auth/register ^
  -H "Content-Type: application/json" ^
  -d "{\"name\":\"أحمد\",\"email\":\"ahmed@test.com\",\"password\":\"123456\"}"
```

### 2. Login
```bash
curl -X POST http://localhost:3001/api/auth/login ^
  -H "Content-Type: application/json" ^
  -d "{\"email\":\"ahmed@test.com\",\"password\":\"123456\"}"
```

احفظ الـ `accessToken` من الرد.

### 3. Test Chat
```bash
curl -X POST http://localhost:3001/api/ai/chat ^
  -H "Content-Type: application/json" ^
  -H "Authorization: Bearer YOUR_TOKEN" ^
  -d "{\"message\":\"ما هي أعراض السكتة الدماغية؟\"}"
```

---

## المشاكل الشائعة

### Python غير موجود
```bash
# حمّل من
https://www.python.org/downloads/
```

### المنفذ مستخدم
```bash
# في .env غيّر
PORT=3002
```

### خطأ في imports
```bash
# تأكد من virtual environment
cd flask_server
venv\Scripts\activate
```

---

## الخطوة التالية

اقرأ `README.md` للتفاصيل الكاملة.

---

**تم! 🎉**

Flask backend يعمل الآن على المنفذ 3001!
