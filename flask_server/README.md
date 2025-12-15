# NeuroAid Flask Backend Server

## نظرة عامة

هذا هو الـ Backend الرئيسي لتطبيق NeuroAid مكتوب بـ **Flask** (Python) بدلاً من Node.js.

## المميزات

✅ **نفس الوظائف تماماً** كما في Node.js backend  
✅ **نفس الـ APIs** - متوافق 100% مع Flutter app  
✅ **نفس البيانات** - يستخدم نفس ملفات JSON  
✅ **متكامل مع AI Services** - يتصل بخدمات الذكاء الاصطناعي الثلاثة  
✅ **JWT Authentication** - نفس نظام المصادقة  
✅ **File Uploads** - دعم رفع الصور  

---

## التثبيت السريع

### 1. تشغيل Setup
```bash
setup.bat
```

هذا سيقوم بـ:
- التحقق من Python
- إنشاء virtual environment
- تثبيت جميع التبعيات
- إنشاء ملف `.env`

### 2. تشغيل السيرفر
```bash
start_server.bat
```

السيرفر سيعمل على: `http://localhost:3001`

---

## البنية

```
flask_server/
├── app.py                 # التطبيق الرئيسي
├── requirements.txt       # التبعيات
├── .env.example          # مثال للإعدادات
├── .env                  # الإعدادات (سيتم إنشاؤه)
│
├── routes/               # المسارات (APIs)
│   ├── __init__.py
│   ├── auth.py          # تسجيل/دخول
│   ├── users.py         # إدارة المستخدمين
│   ├── doctors.py       # الأطباء
│   ├── bookings.py      # الحجوزات
│   ├── faqs.py          # الأسئلة الشائعة
│   ├── scans.py         # الفحوصات
│   ├── favorites.py     # المفضلة
│   └── ai.py            # خدمات الذكاء الاصطناعي
│
├── utils/               # الأدوات المساعدة
│   ├── __init__.py
│   ├── auth.py         # JWT و Authentication
│   └── database.py     # قراءة/كتابة JSON
│
├── setup.bat           # سكريبت التثبيت
└── start_server.bat    # سكريبت التشغيل
```

---

## الـ APIs المتاحة

جميع الـ APIs نفسها تماماً كما في Node.js backend:

### Authentication
- `POST /api/auth/register` - تسجيل مستخدم جديد
- `POST /api/auth/login` - تسجيل الدخول

### Users
- `GET /api/users` - جميع المستخدمين (admin فقط)
- `GET /api/users/me` - بيانات المستخدم الحالي

### AI Services
- `POST /api/ai/chat` - المحادثة الذكية
- `POST /api/ai/stroke-assessment` - تقييم المخاطر
- `POST /api/ai/scan-image` - تحليل الصور

### Doctors
- `GET /api/doctors` - جميع الأطباء
- `GET /api/doctors/:id` - طبيب محدد

### Bookings
- `GET /api/bookings` - حجوزات المستخدم
- `POST /api/bookings` - حجز جديد
- `DELETE /api/bookings/:id` - إلغاء حجز

### FAQs
- `GET /api/faqs` - الأسئلة الشائعة

### Scans
- `GET /api/scans` - فحوصات المستخدم
- `POST /api/scans` - رفع فحص جديد
- `DELETE /api/scans/:id` - حذف فحص

### Favorites
- `GET /api/favorites` - الأطباء المفضلين
- `POST /api/favorites` - إضافة للمفضلة
- `DELETE /api/favorites/:id` - إزالة من المفضلة

---

## الإعدادات (.env)

```env
PORT=3001
NODE_ENV=development

# AI Services
AI_CHATBOT_URL=http://localhost:5001
AI_STROKE_QA_URL=http://localhost:5002
AI_STROKE_IMAGE_URL=http://localhost:5003

# JWT
JWT_SECRET=your-secret-key-change-this-in-production
JWT_EXPIRES_IN=7d

# Database
DB_PATH=./data/db.json

# Uploads
MAX_FILE_SIZE=10485760
UPLOAD_PATH=./uploads
```

---

## التشغيل اليدوي

إذا أردت التشغيل بدون batch files:

```bash
# إنشاء virtual environment
python -m venv venv

# تفعيل virtual environment
venv\Scripts\activate

# تثبيت التبعيات
pip install -r requirements.txt

# نسخ .env
copy .env.example .env

# تشغيل السيرفر
python app.py
```

---

## الفروقات عن Node.js Backend

### المتشابه ✅
- جميع الـ APIs نفسها
- نفس البيانات (JSON files)
- نفس المنطق والوظائف
- نفس نظام JWT
- نفس التكامل مع AI services

### المختلف 🔄
- اللغة: Python بدلاً من JavaScript
- Framework: Flask بدلاً من Express
- Password hashing: Werkzeug بدلاً من bcryptjs
- Virtual environment بدلاً من node_modules

---

## التكامل مع AI Services

السيرفر يتصل تلقائياً بخدمات الذكاء الاصطناعي الثلاثة:

1. **Chatbot** (Port 5001)
2. **Stroke Assessment** (Port 5002)
3. **Image Analysis** (Port 5003)

إذا لم تكن الخدمات متاحة، سيستخدم mock responses.

---

## الاختبار

### Health Check
```bash
curl http://localhost:3001/health
```

### Register
```bash
curl -X POST http://localhost:3001/api/auth/register ^
  -H "Content-Type: application/json" ^
  -d "{\"name\":\"Test User\",\"email\":\"test@example.com\",\"password\":\"password123\"}"
```

### Login
```bash
curl -X POST http://localhost:3001/api/auth/login ^
  -H "Content-Type: application/json" ^
  -d "{\"email\":\"test@example.com\",\"password\":\"password123\"}"
```

---

## حل المشاكل

### Python غير موجود
```bash
# تحميل Python من
https://www.python.org/downloads/
```

### خطأ في التبعيات
```bash
# حدّث pip
python -m pip install --upgrade pip

# أعد التثبيت
pip install -r requirements.txt
```

### المنفذ مستخدم
```bash
# غيّر PORT في .env
PORT=3002
```

### خطأ في الـ imports
```bash
# تأكد من تفعيل virtual environment
venv\Scripts\activate
```

---

## النشر للإنتاج

### استخدام Gunicorn
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:3001 app:app
```

### استخدام Waitress (Windows)
```bash
pip install waitress
waitress-serve --port=3001 app:app
```

---

## المقارنة

| Feature | Node.js | Flask |
|---------|---------|-------|
| Language | JavaScript | Python |
| Framework | Express | Flask |
| Performance | ⚡ Very Fast | ⚡ Fast |
| Ease of Use | ✅ Easy | ✅ Very Easy |
| AI Integration | ✅ Good | ✅ Excellent |
| Community | 🌟 Huge | 🌟 Huge |

---

## لماذا Flask؟

1. **توحيد اللغة** - كل الـ backend بـ Python (مع AI services)
2. **سهولة التطوير** - Python أسهل للكثيرين
3. **تكامل أفضل** - مع مكتبات ML/AI
4. **نفس الوظائف** - لا فرق من ناحية المستخدم

---

## الدعم

للمساعدة:
1. راجع التوثيق أعلاه
2. تحقق من `../API_DOCUMENTATION.md`
3. تواصل مع فريق التطوير

---

**جاهز للاستخدام! 🚀**

Flask backend جاهز ويعمل بنفس كفاءة Node.js backend!
