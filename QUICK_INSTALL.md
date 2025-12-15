# 🚀 NeuroAid Backend - دليل التثبيت السريع

## التثبيت التلقائي (موصى به)

### على Windows:
```bash
install.bat
```

هذا الملف سيقوم بـ:
- ✅ التحقق من تثبيت Python
- ✅ إنشاء البيئة الافتراضية (virtual environment)
- ✅ تثبيت جميع المكتبات المطلوبة
- ✅ التحقق من التثبيت

## التثبيت اليدوي

### 1. إنشاء البيئة الافتراضية
```bash
python -m venv venv
```

### 2. تفعيل البيئة الافتراضية
```bash
# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

### 3. تثبيت المكتبات
```bash
pip install -r requirements.txt
```

### 4. التحقق من التثبيت
```bash
python verify_installation.py
```

## إعداد البيئة

```bash
# نسخ ملف المثال
copy .env.example .env

# ثم عدّل .env وأضف:
# - OPENAI_API_KEY (للـ chatbot)
# - JWT_SECRET (للأمان)
```

## تشغيل المشروع

```bash
# تشغيل جميع الخدمات
python run_system.py

# أو
python gateway.py
```

## المكتبات المطلوبة

### Core Services
- Flask 3.0.0
- Flask-CORS 4.0.0
- Python-dotenv 1.0.0

### AI Chatbot
- LangGraph
- LangChain
- OpenAI SDK
- LangSmith

### Machine Learning
- TensorFlow 2.13.0
- Keras
- NumPy
- Scikit-learn
- Pandas

### Image Processing
- Pillow

### Async Support
- aiohttp

## استكشاف الأخطاء

### TensorFlow لا يعمل
```bash
# جرب نسخة CPU فقط
pip install tensorflow-cpu==2.13.0
```

### LangChain/OpenAI مفقود
```bash
# تثبيت يدوي
pip install langgraph langchain langchain-openai openai
```

## للمزيد من المعلومات

راجع `DEPLOYMENT_GUIDE.md` للحصول على دليل شامل.

---
**Happy Coding! 🚀**
