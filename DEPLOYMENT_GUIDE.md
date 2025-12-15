# 🚀 NeuroAid Backend - دليل التثبيت السريع للـ VM

## 📋 المتطلبات الأساسية

قبل البدء، تأكد من تثبيت:
- **Python 3.9 أو أحدث** - [تحميل Python](https://www.python.org/downloads/)
- **Git** (اختياري) - لتحميل المشروع

## 🔧 خطوات التثبيت

### 1. تحميل المشروع

```bash
# إذا كنت تستخدم Git
git clone <repository-url>
cd backend

# أو قم بنسخ المجلد مباشرة إلى الـ VM
```

### 2. إنشاء البيئة الافتراضية (Virtual Environment)

```bash
# إنشاء البيئة الافتراضية
python -m venv venv

# تفعيل البيئة الافتراضية
# على Windows:
venv\Scripts\activate

# على Linux/Mac:
source venv/bin/activate
```

### 3. تثبيت جميع المكتبات المطلوبة

```bash
# تثبيت جميع المكتبات دفعة واحدة
pip install -r requirements.txt
```

**ملاحظة:** قد يستغرق التثبيت بعض الوقت خاصة TensorFlow (حوالي 5-10 دقائق).

### 4. إعداد ملف البيئة (.env)

```bash
# نسخ ملف المثال
copy .env.example .env

# ثم قم بتعديل .env حسب إعدادات الـ VM الخاصة بك
```

**محتوى ملف .env الأساسي:**
```env
# Server Configuration
FLASK_ENV=production
FLASK_DEBUG=False
HOST=0.0.0.0
PORT=3001

# AI Services URLs
CHATBOT_SERVICE_URL=http://localhost:5001
STROKE_QA_SERVICE_URL=http://localhost:5002
STROKE_IMAGE_SERVICE_URL=http://localhost:5003

# Security
JWT_SECRET=your-super-secret-key-change-this-in-production
```

### 5. التحقق من التثبيت

```bash
# التحقق من نسخة Python
python --version

# التحقق من المكتبات المثبتة
pip list

# التحقق من Flask
python -c "import flask; print(f'Flask version: {flask.__version__}')"

# التحقق من TensorFlow
python -c "import tensorflow as tf; print(f'TensorFlow version: {tf.__version__}')"
```

## 🚀 تشغيل المشروع

### الطريقة 1: تشغيل كل الخدمات معاً (موصى بها)

```bash
# على Windows
python run_system.py

# أو استخدم الـ batch file
start_all_servers.bat
```

### الطريقة 2: تشغيل كل خدمة على حدة

```bash
# Terminal 1: Flask Main Server
cd flask_server
python app.py

# Terminal 2: Chatbot Service
cd ai_services/chatbot
python app.py

# Terminal 3: Stroke Assessment
cd ai_services/stroke_assessment
python app.py

# Terminal 4: Stroke Image Analysis
cd ai_services/stroke_image
python app.py
```

### الطريقة 3: استخدام API Gateway (الأفضل)

```bash
# تشغيل الـ Gateway فقط (يدير كل الخدمات)
python gateway.py
```

## 🧪 اختبار التثبيت

بعد تشغيل الخدمات، اختبر الـ endpoints:

```bash
# اختبار Flask Main Server
curl http://localhost:3001/api/health

# اختبار Chatbot
curl http://localhost:5001/health

# اختبار Stroke Assessment
curl http://localhost:5002/health

# اختبار Image Analysis
curl http://localhost:5003/health
```

أو استخدم الـ batch file للاختبار:
```bash
test_endpoints.bat
```

## 📊 المنافذ المستخدمة

| الخدمة | المنفذ | الوصف |
|--------|--------|-------|
| Flask Main Server | 3001 | السيرفر الرئيسي |
| API Gateway | 8080 | بوابة API الموحدة |
| Chatbot Service | 5001 | خدمة المحادثة الذكية |
| Stroke Assessment | 5002 | تقييم خطر السكتة |
| Image Analysis | 5003 | تحليل صور الأشعة |

## 🔥 إعداد Firewall (مهم للـ LAN)

إذا كنت تريد الوصول للخدمات من أجهزة أخرى على الشبكة:

```bash
# على Windows (كـ Administrator)
configure_firewall.bat
```

أو يدوياً:
```bash
netsh advfirewall firewall add rule name="NeuroAid Flask" dir=in action=allow protocol=TCP localport=3001
netsh advfirewall firewall add rule name="NeuroAid Gateway" dir=in action=allow protocol=TCP localport=8080
netsh advfirewall firewall add rule name="NeuroAid Chatbot" dir=in action=allow protocol=TCP localport=5001
netsh advfirewall firewall add rule name="NeuroAid Stroke QA" dir=in action=allow protocol=TCP localport=5002
netsh advfirewall firewall add rule name="NeuroAid Image" dir=in action=allow protocol=TCP localport=5003
```

## 🐛 حل المشاكل الشائعة

### مشكلة: "pip not found"
```bash
# تأكد من تثبيت Python بشكل صحيح
python -m ensurepip --upgrade
```

### مشكلة: "TensorFlow installation failed"
```bash
# جرب تثبيت نسخة أقدم
pip install tensorflow==2.12.0

# أو استخدم CPU version فقط
pip install tensorflow-cpu==2.13.0
```

### مشكلة: "Port already in use"
```bash
# ابحث عن العملية المستخدمة للمنفذ
netstat -ano | findstr :3001

# أوقف العملية
taskkill /PID <process_id> /F
```

### مشكلة: "Module not found"
```bash
# تأكد من تفعيل البيئة الافتراضية
venv\Scripts\activate

# أعد تثبيت المكتبات
pip install -r requirements.txt
```

## 📦 متطلبات النظام الموصى بها

- **المعالج:** Intel i5 أو أفضل
- **الذاكرة:** 8 GB RAM على الأقل (16 GB موصى به)
- **المساحة:** 5 GB مساحة فارغة
- **نظام التشغيل:** Windows 10/11, Ubuntu 20.04+, macOS 10.15+

## 🔐 ملاحظات الأمان للـ Production

1. **غير JWT_SECRET** في ملف `.env`
2. **عطل DEBUG mode** في production
3. **استخدم HTTPS** بدلاً من HTTP
4. **قيّد CORS** للدومينات المسموحة فقط
5. **استخدم gunicorn** أو **waitress** بدلاً من Flask development server

### تثبيت Gunicorn للـ Production:
```bash
pip install gunicorn

# تشغيل مع gunicorn
gunicorn -w 4 -b 0.0.0.0:3001 flask_server.app:app
```

## 📚 ملفات مرجعية إضافية

- `README.md` - نظرة عامة على المشروع
- `INSTALLATION_GUIDE.md` - دليل تفصيلي للتثبيت
- `API_DOCUMENTATION.md` - توثيق الـ API (إن وجد)

## ✅ قائمة التحقق النهائية

- [ ] Python 3.9+ مثبت
- [ ] Virtual environment تم إنشاؤه وتفعيله
- [ ] جميع المكتبات من requirements.txt مثبتة
- [ ] ملف .env تم إعداده
- [ ] Firewall تم تكوينه (للـ LAN)
- [ ] جميع الخدمات تعمل بنجاح
- [ ] الـ endpoints تستجيب بشكل صحيح

## 🆘 الدعم

للمساعدة أو الإبلاغ عن مشاكل، تواصل مع فريق التطوير.

---

**Happy Deployment! 🚀**
