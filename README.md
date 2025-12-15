# NeuroAid Backend Server

Backend موحد لتطبيق NeuroAid مع دعم كامل للـ AI Services

## 🚀 البدء السريع

### 1. التثبيت

```bash
cd backend
npm install
```

### 2. إعداد البيئة

انسخ ملف `.env.example` إلى `.env`:

```bash
copy .env.example .env
```

عدّل الإعدادات في `.env` حسب الحاجة.

### 3. تشغيل السيرفر

```bash
npm start
```

أو للتطوير مع auto-reload:

```bash
npm run dev
```

## 📱 الاتصال من التطبيق

### Android Emulator
```
http://10.0.2.2:3001
```

### iOS Simulator
```
http://localhost:3001
```

### Physical Device
استخدم عنوان IP الخاص بجهازك:
```
http://192.168.x.x:3001
```

## 🔐 المصادقة (Authentication)

### تسجيل مستخدم جديد

**Endpoint:** `POST /api/auth/register`

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "password123",
  "name": "أحمد محمد",
  "phone": "+20 100 123 4567",
  "role": "user"
}
```

**Response:**
```json
{
  "accessToken": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "user": {
    "id": 1,
    "email": "user@example.com",
    "name": "أحمد محمد",
    "phone": "+20 100 123 4567",
    "role": "user",
    "isActive": true,
    "createdAt": "2025-12-07T11:19:31.000Z"
  }
}
```

### تسجيل الدخول

**Endpoint:** `POST /api/auth/login`

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "password123"
}
```

**Response:** نفس استجابة التسجيل

## 🤖 AI Services

جميع endpoints الخاصة بالـ AI تحتاج إلى Authentication Token في الـ header:

```
Authorization: Bearer YOUR_TOKEN_HERE
```

### 1. AI Chatbot

**Endpoint:** `POST /api/ai/chat`

**Request Body:**
```json
{
  "message": "ما هي أعراض السكتة الدماغية؟",
  "conversationHistory": [
    {
      "role": "user",
      "content": "مرحباً"
    },
    {
      "role": "assistant",
      "content": "مرحباً بك! كيف يمكنني مساعدتك؟"
    }
  ]
}
```

**Response:**
```json
{
  "response": "أعراض السكتة الدماغية تشمل...",
  "timestamp": "2025-12-07T11:19:31.000Z"
}
```

### 2. تقييم خطر السكتة الدماغية

**Endpoint:** `POST /api/ai/stroke-assessment`

**Request Body:**
```json
{
  "age": 65,
  "gender": "male",
  "hypertension": 1,
  "heartDisease": 0,
  "everMarried": "Yes",
  "workType": "Private",
  "residenceType": "Urban",
  "avgGlucoseLevel": 120,
  "bmi": 28.5,
  "smokingStatus": "formerly smoked"
}
```

**Response:**
```json
{
  "riskLevel": "medium",
  "riskPercentage": 45,
  "recommendations": [
    "استشر طبيبك بانتظام",
    "مارس الرياضة يومياً",
    "اتبع نظام غذائي صحي",
    "راقب ضغط الدم بانتظام",
    "تجنب التدخين السلبي"
  ],
  "timestamp": "2025-12-07T11:19:31.000Z"
}
```

### 3. تحليل صورة السكتة الدماغية

**Endpoint:** `POST /api/ai/scan-image`

**Request:** Multipart Form Data
```
image: [File]
```

**Response:**
```json
{
  "scanId": 1733571571000,
  "result": "normal",
  "confidence": 0.87,
  "findings": [
    "لا توجد علامات واضحة للسكتة الدماغية",
    "الصورة تبدو طبيعية"
  ],
  "imageUrl": "/uploads/scans/scan-1733571571000-123456789.jpg",
  "timestamp": "2025-12-07T11:19:31.000Z"
}
```

## 📊 إدارة الفحوصات (Scans)

### الحصول على جميع الفحوصات

**Endpoint:** `GET /api/scans`

**Headers:**
```
Authorization: Bearer YOUR_TOKEN_HERE
```

**Response:**
```json
[
  {
    "id": 1,
    "userId": 1,
    "result": "normal",
    "confidence": 0.87,
    "findings": ["لا توجد علامات واضحة للسكتة الدماغية"],
    "imageUrl": "/uploads/scans/scan-123.jpg",
    "createdAt": "2025-12-07T11:19:31.000Z"
  }
]
```

### الحصول على فحص محدد

**Endpoint:** `GET /api/scans/:id`

### حفظ نتيجة فحص جديد

**Endpoint:** `POST /api/scans`

**Request Body:**
```json
{
  "result": "normal",
  "confidence": 0.87,
  "findings": ["لا توجد علامات واضحة للسكتة الدماغية"],
  "imageUrl": "/uploads/scans/scan-123.jpg"
}
```

### حذف فحص

**Endpoint:** `DELETE /api/scans/:id`

## 👨‍⚕️ الأطباء (Doctors)

### الحصول على جميع الأطباء

**Endpoint:** `GET /api/doctors`

**Response:**
```json
[
  {
    "id": 1,
    "name": "د. أحمد حسن",
    "specialty": "أخصائي الأعصاب",
    "experience": "15 سنة",
    "rating": 4.8,
    "image": "/uploads/doctors/doctor1.jpg",
    "phone": "+20 100 123 4567",
    "email": "ahmed.hassan@neuroaid.com"
  }
]
```

### الحصول على طبيب محدد

**Endpoint:** `GET /api/doctors/:id`

## 📅 الحجوزات (Bookings)

### الحصول على جميع الحجوزات

**Endpoint:** `GET /api/bookings`

**Headers:**
```
Authorization: Bearer YOUR_TOKEN_HERE
```

### إنشاء حجز جديد

**Endpoint:** `POST /api/bookings`

**Request Body:**
```json
{
  "doctorId": 1,
  "date": "2025-12-15",
  "time": "10:00",
  "notes": "استشارة أولية"
}
```

### تحديث حجز

**Endpoint:** `PUT /api/bookings/:id`

**Request Body:**
```json
{
  "date": "2025-12-16",
  "time": "11:00",
  "status": "confirmed"
}
```

### حذف حجز

**Endpoint:** `DELETE /api/bookings/:id`

## ❓ الأسئلة الشائعة (FAQs)

### الحصول على جميع الأسئلة

**Endpoint:** `GET /api/faqs`

### الحصول على سؤال محدد

**Endpoint:** `GET /api/faqs/:id`

## 👤 المستخدمين (Users)

### الحصول على ملف المستخدم الحالي

**Endpoint:** `GET /api/users/me`

**Headers:**
```
Authorization: Bearer YOUR_TOKEN_HERE
```

### الحصول على جميع المستخدمين (Admin فقط)

**Endpoint:** `GET /api/users`

## 🔧 دمج خدمات الـ AI

حالياً، الـ backend يعمل بنظام **fallback** ذكي:

1. **إذا كانت خدمات الـ AI متاحة:** يتم الاتصال بها وإرجاع النتائج الحقيقية
2. **إذا لم تكن متاحة:** يتم إرجاع نتائج mock واقعية

### لتفعيل خدمات الـ AI:

1. قم بتشغيل خوادم الـ AI على المنافذ المحددة:
   - Chatbot: `http://localhost:5001`
   - Stroke QA: `http://localhost:5002`
   - Stroke Image: `http://localhost:5003`

2. تأكد من أن الـ endpoints التالية متاحة:
   - `POST /chat` للـ chatbot
   - `POST /predict` للـ stroke assessment
   - `POST /analyze` للـ image analysis

3. الـ backend سيتعرف تلقائياً على توفر الخدمات ويستخدمها

## 📁 هيكل المشروع

```
backend/
├── server.js              # Main server file
├── package.json           # Dependencies
├── .env                   # Environment variables
├── middleware/
│   └── auth.js           # JWT authentication
├── routes/
│   ├── auth.js           # Authentication routes
│   ├── users.js          # User management
│   ├── ai.js             # AI services
│   ├── scans.js          # Scan management
│   ├── doctors.js        # Doctors info
│   ├── bookings.js       # Appointment booking
│   └── faqs.js           # FAQs
├── data/                  # JSON databases
│   ├── users.json
│   ├── scans.json
│   ├── bookings.json
│   └── doctors.json
└── uploads/               # Uploaded files
    └── scans/
```

## 🐛 استكشاف الأخطاء

### لا يمكن الاتصال من التطبيق

1. تأكد من تشغيل السيرفر (`npm start`)
2. تحقق من إعدادات الـ Firewall
3. للـ Android Emulator، استخدم `10.0.2.2` بدلاً من `localhost`
4. للأجهزة الفعلية، تأكد من أن الجهاز والكمبيوتر على نفس الشبكة

### أخطاء المصادقة

1. تأكد من إرسال الـ token في الـ header
2. تحقق من صلاحية الـ token
3. تأكد من أن المستخدم لديه الصلاحيات المطلوبة

### أخطاء رفع الصور

1. تأكد من أن حجم الصورة أقل من 10MB
2. تحقق من نوع الملف (jpg, jpeg, png, gif فقط)
3. تأكد من وجود مجلد `uploads/scans`

## 📝 ملاحظات مهمة

- **الأمان:** غيّر `JWT_SECRET` في production
- **البيانات:** حالياً يتم حفظ البيانات في ملفات JSON، يمكن الترقية لقاعدة بيانات حقيقية لاحقاً
- **AI Services:** النظام يعمل بدون خدمات AI (mock mode) حتى يتم تفعيلها
- **CORS:** مفعّل لجميع المصادر، قد تحتاج لتقييده في production

## 🎯 الخطوات التالية

1. ✅ تشغيل الـ backend
2. ⏳ تفعيل خدمات الـ AI
3. ⏳ ربط التطبيق بالـ backend
4. ⏳ اختبار جميع الـ endpoints
5. ⏳ إضافة المزيد من الميزات

## 🆘 الدعم

للمساعدة أو الإبلاغ عن مشاكل، تواصل مع فريق التطوير.

---

**Happy Coding! 🚀**
