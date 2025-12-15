# 🚀 دليل تثبيت وتشغيل الباك إند - NeuroAid

## 📋 المحتويات
1. [المتطلبات الأساسية](#المتطلبات-الأساسية)
2. [خطوات التثبيت](#خطوات-التثبيت)
3. [إعداد البيئة](#إعداد-البيئة)
4. [تشغيل السيرفرات](#تشغيل-السيرفرات)
5. [التحقق من التشغيل](#التحقق-من-التشغيل)
6. [حل المشاكل الشائعة](#حل-المشاكل-الشائعة)

---

## 💻 المتطلبات الأساسية

### 1. تثبيت Python

**تحميل Python:**
- اذهب إلى: https://www.python.org/downloads/
- حمل **Python 3.8** أو أحدث
- **مهم جداً:** أثناء التثبيت، ✅ فعّل خيار **"Add Python to PATH"**

**التحقق من التثبيت:**
```bash
python --version
```
يجب أن ترى: `Python 3.x.x`

إذا لم يعمل، جرب:
```bash
python3 --version
```

---

### 2. تثبيت pip (مدير الحزم)

عادةً يأتي مع Python، للتحقق:
```bash
pip --version
```

إذا لم يعمل:
```bash
python -m pip --version
```

---

### 3. الحصول على Gemini API Key (للـ Chatbot)

**الخطوات:**
1. اذهب إلى: https://makersuite.google.com/app/apikey
2. سجل دخول بحساب Google
3. اضغط **"Create API Key"**
4. انسخ الـ API Key (هتحتاجه بعدين)

**مثال على API Key:**
```
AIzaSyDXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
```

---

## 📥 خطوات التثبيت

### الخطوة 1: نسخ المشروع

**إذا كان عندك المشروع على USB أو مجلد:**
```bash
# انسخ مجلد backend لأي مكان على جهازك
# مثلاً: C:\Projects\neuroaid\backend
```

**إذا كان على GitHub:**
```bash
git clone https://github.com/your-repo/neuroaid.git
cd neuroaid/backend
```

---

### الخطوة 2: تثبيت المكتبات الأساسية

افتح **Command Prompt** أو **PowerShell** في مجلد `backend`:

```bash
cd path/to/backend
pip install -r requirements.txt
```

**إذا ظهرت مشاكل، جرب:**
```bash
python -m pip install -r requirements.txt
```

**المكتبات اللي هتتثبت:**
- Flask (السيرفر الرئيسي)
- flask-cors (للسماح بالاتصال من التطبيق)
- requests (للاتصال بين السيرفرات)
- python-dotenv (لقراءة ملفات .env)

---

### الخطوة 3: تثبيت مكتبات Flask Server

```bash
cd flask_server
pip install -r requirements.txt
```

**المكتبات:**
- Flask
- flask-cors
- werkzeug (للتشفير)
- PyJWT (للـ tokens)

---

### الخطوة 4: تثبيت مكتبات AI Services

#### أ) Chatbot Service
```bash
cd ai_services/chatbot
pip install -r requirements.txt
```

**المكتبات:**
- Flask
- google-generativeai (Gemini AI)

#### ب) Stroke Assessment Service
```bash
cd ../stroke_assessment
pip install -r requirements.txt
```

**المكتبات:**
- Flask
- scikit-learn (للـ ML Model)
- numpy
- pandas

#### ج) Image Analysis Service
```bash
cd ../stroke_image
pip install -r requirements.txt
```

**المكتبات:**
- Flask
- tensorflow أو keras (للـ Deep Learning)
- Pillow (لمعالجة الصور)
- numpy

---

## ⚙️ إعداد البيئة

### 1. إعداد Gateway (.env في مجلد backend)

**إنشاء ملف `.env`:**
```bash
cd backend
copy .env.example .env
```

**محتوى الملف:**
```env
GATEWAY_PORT=8080
```

---

### 2. إعداد Flask Server (.env في flask_server)

```bash
cd flask_server
copy .env.example .env
```

**عدّل الملف `.env`:**
```env
PORT=5000
JWT_SECRET=your_super_secret_key_change_this_12345
JWT_EXPIRES_IN=7d
MAX_FILE_SIZE=10485760
UPLOAD_PATH=./uploads
NODE_ENV=development
```

**⚠️ مهم:**
- غيّر `JWT_SECRET` لأي نص عشوائي طويل (للأمان)

---

### 3. إعداد Chatbot Service (.env في ai_services/chatbot)

```bash
cd ai_services/chatbot
copy .env.example .env
```

**عدّل الملف `.env`:**
```env
GEMINI_API_KEY=AIzaSyDXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
PORT=5001
```

**⚠️ مهم:**
- ضع الـ Gemini API Key اللي حصلت عليه

---

### 4. إعداد Stroke Assessment (.env في ai_services/stroke_assessment)

```bash
cd ai_services/stroke_assessment
```

**إنشاء ملف `.env` (إذا لم يكن موجود):**
```env
PORT=5002
```

---

### 5. إعداد Image Analysis (.env في ai_services/stroke_image)

```bash
cd ai_services/stroke_image
```

**إنشاء ملف `.env` (إذا لم يكن موجود):**
```env
PORT=5003
```

---

## 🚀 تشغيل السيرفرات

### الطريقة السهلة (Windows):

**استخدم الملف الجاهز:**
```bash
cd backend
start_all_servers.bat
```

هيفتح 5 نوافذ Command Prompt، كل واحدة لسيرفر.

---

### الطريقة اليدوية:

افتح **5 نوافذ Command Prompt** منفصلة:

#### النافذة 1: API Gateway
```bash
cd backend
python gateway.py
```

**يجب أن ترى:**
```
🚀 NeuroAid API Gateway Started
Gateway: http://192.168.x.x:8080
```

---

#### النافذة 2: Flask Main Server
```bash
cd backend/flask_server
python app.py
```

**يجب أن ترى:**
```
>> NeuroAid Backend Server Started (Flask)!
Server URL: http://localhost:5000
```

---

#### النافذة 3: AI Chatbot
```bash
cd backend/ai_services/chatbot
python app.py
```

**يجب أن ترى:**
```
🤖 AI Chatbot Service Started
Running on http://127.0.0.1:5001
```

---

#### النافذة 4: Stroke Assessment
```bash
cd backend/ai_services/stroke_assessment
python app.py
```

**يجب أن ترى:**
```
📊 Stroke Assessment Service Started
Running on http://127.0.0.1:5002
```

---

#### النافذة 5: Image Analysis
```bash
cd backend/ai_services/stroke_image
python app.py
```

**يجب أن ترى:**
```
🖼️ Image Analysis Service Started
Running on http://127.0.0.1:5003
```

---

## ✅ التحقق من التشغيل

### 1. فحص الـ Gateway

افتح المتصفح واذهب إلى:
```
http://localhost:8080/health
```

**يجب أن ترى:**
```json
{
  "gateway": "OK",
  "timestamp": "2025-12-15T15:00:00",
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
    },
    "ai_image": {
      "status": "online",
      "url": "http://127.0.0.1:5003"
    }
  }
}
```

**✅ إذا كل الـ services "online"، معناها كل حاجة شغالة!**

---

### 2. فحص Flask Server

```
http://localhost:5000/health
```

**يجب أن ترى:**
```json
{
  "status": "OK",
  "message": "NeuroAid Backend Server is running (Flask)",
  "services": {
    "auth": "active",
    "ai": "active",
    "database": "active"
  }
}
```

---

### 3. اختبار من الموبايل

**احصل على IP Address بتاع الجهاز:**

**Windows:**
```bash
ipconfig
```
ابحث عن **"IPv4 Address"** تحت **"Wireless LAN adapter Wi-Fi"**

مثال: `192.168.1.10`

**من الموبايل، افتح المتصفح:**
```
http://192.168.1.10:8080/health
```

**⚠️ تأكد:**
- الموبايل والكمبيوتر على نفس الـ WiFi
- الـ Firewall مش بيمنع الاتصال

---

## 🔧 حل المشاكل الشائعة

### ❌ مشكلة: "python is not recognized"

**الحل:**
1. تأكد إنك ثبّت Python صح
2. أثناء التثبيت، فعّل **"Add Python to PATH"**
3. أعد تشغيل Command Prompt
4. إذا لم ينفع، استخدم المسار الكامل:
```bash
C:\Users\YourName\AppData\Local\Programs\Python\Python311\python.exe gateway.py
```

---

### ❌ مشكلة: "No module named 'flask'"

**الحل:**
```bash
pip install flask
```

أو:
```bash
python -m pip install flask
```

---

### ❌ مشكلة: "Port 5000 is already in use"

**الحل:**
1. أوقف البرنامج اللي شغال على Port 5000
2. أو غيّر الـ Port في `.env`:
```env
PORT=5050
```

**للبحث عن البرنامج (Windows):**
```bash
netstat -ano | findstr :5000
taskkill /PID <رقم_العملية> /F
```

---

### ❌ مشكلة: "Invalid API Key" (Gemini)

**الحل:**
1. تأكد إنك نسخت الـ API Key صح (بدون مسافات)
2. تأكد إن الـ API Key مفعّل على Google AI Studio
3. جرب API Key جديد

---

### ❌ مشكلة: "Can't connect from mobile"

**الحل:**
1. تأكد إن الموبايل والكمبيوتر على نفس الـ WiFi
2. افتح الـ Firewall:
```bash
# شغل كـ Administrator
netsh advfirewall firewall add rule name="NeuroAid Backend" dir=in action=allow protocol=TCP localport=8080
```

3. أو استخدم الملف الجاهز:
```bash
cd backend
configure_firewall.bat
```

---

### ❌ مشكلة: "Service offline" في /health

**الحل:**
1. تأكد إن السيرفر شغال في نافذة منفصلة
2. شوف رسائل الخطأ في نافذة السيرفر
3. تأكد إن الـ Port مش مستخدم من برنامج تاني

---

## 📱 ربط التطبيق بالباك إند

بعد ما تشغل الباك إند، محتاج تعدل في التطبيق:

**في Flutter App:**

ملف: `lib/core/constants/api_constants.dart`

```dart
class ApiConstants {
  // ضع IP Address بتاع الجهاز هنا
  static const String _networkIp = '192.168.1.10'; // غيّر ده
  
  static const String _gatewayPort = '8080';
  
  static String get baseUrl {
    if (kDebugMode) {
      return 'http://$_networkIp:$_gatewayPort';
    }
    return 'http://localhost:$_gatewayPort';
  }
}
```

---

## 📊 ملخص الـ Ports

| السيرفر | Port | URL |
|---------|------|-----|
| API Gateway | 8080 | http://localhost:8080 |
| Flask Main Server | 5000 | http://localhost:5000 |
| AI Chatbot | 5001 | http://localhost:5001 |
| Stroke Assessment | 5002 | http://localhost:5002 |
| Image Analysis | 5003 | http://localhost:5003 |

---

## 🎯 Checklist النهائي

قبل ما تقول "الباك إند شغال"، تأكد من:

- [ ] Python مثبت (version 3.8+)
- [ ] كل المكتبات اتثبتت بنجاح
- [ ] ملفات `.env` موجودة ومعدّلة
- [ ] Gemini API Key صحيح
- [ ] الـ 5 سيرفرات شغالة
- [ ] `/health` بيرجع "OK" لكل السيرفرات
- [ ] الموبايل يقدر يتصل بالباك إند

---

## 🆘 محتاج مساعدة؟

**إذا واجهت مشكلة:**

1. شوف رسائل الخطأ في نافذة Command Prompt
2. تأكد إن كل الخطوات اتنفذت بالترتيب
3. جرب تعيد تشغيل السيرفرات
4. تأكد من الـ Firewall والـ Antivirus

---

## 📝 ملاحظات مهمة

- **لا تغلق نوافذ Command Prompt** طول ما الباك إند شغال
- **لو عايز توقف السيرفرات:** اضغط `Ctrl+C` في كل نافذة
- **البيانات بتتحفظ في:** `backend/data/` (JSON files)
- **الصور بتتحفظ في:** `backend/flask_server/uploads/`

---

**بالتوفيق! 🚀**

إذا كل حاجة شغالة، يبقى جاهز تستخدم التطبيق! 🎉
