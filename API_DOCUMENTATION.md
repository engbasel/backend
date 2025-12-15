# NeuroAid Backend API Documentation

## Base URL
```
http://localhost:3001/api
```

For mobile devices on the same network, replace `localhost` with your computer's IP address (e.g., `http://192.168.1.27:3001/api`)

---

## Authentication

Most endpoints require authentication. Include the JWT token in the Authorization header:

```
Authorization: Bearer <your_jwt_token>
```

### Register
**POST** `/auth/register`

Register a new user account.

**Request Body:**
```json
{
  "name": "أحمد محمد",
  "email": "ahmed@example.com",
  "password": "password123",
  "phone": "01234567890",
  "dateOfBirth": "1990-01-01",
  "gender": "male"
}
```

**Response:**
```json
{
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "user": {
    "id": "user123",
    "name": "أحمد محمد",
    "email": "ahmed@example.com",
    "phone": "01234567890"
  }
}
```

### Login
**POST** `/auth/login`

Login with existing credentials.

**Request Body:**
```json
{
  "email": "ahmed@example.com",
  "password": "password123"
}
```

**Response:**
```json
{
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "user": {
    "id": "user123",
    "name": "أحمد محمد",
    "email": "ahmed@example.com"
  }
}
```

---

## AI Services

### 1. AI Chatbot
**POST** `/ai/chat`

Chat with AI assistant about stroke-related questions.

**Headers:**
```
Authorization: Bearer <token>
Content-Type: application/json
```

**Request Body:**
```json
{
  "message": "ما هي أعراض السكتة الدماغية؟",
  "conversationHistory": [
    {
      "role": "user",
      "content": "مرحبا"
    },
    {
      "role": "assistant",
      "content": "مرحباً! كيف يمكنني مساعدتك؟"
    }
  ]
}
```

**Response:**
```json
{
  "response": "أعراض السكتة الدماغية الرئيسية تشمل:\n• ضعف مفاجئ في الوجه أو الذراع أو الساق\n• صعوبة في الكلام أو الفهم\n• مشاكل في الرؤية...",
  "timestamp": "2024-12-07T19:30:00.000Z"
}
```

**Possible Questions:**
- "ما هي أعراض السكتة الدماغية؟"
- "كيف يمكن الوقاية من السكتة الدماغية؟"
- "ما هي عوامل الخطر؟"
- "ما هو العلاج المتاح؟"

---

### 2. Stroke Risk Assessment
**POST** `/ai/stroke-assessment`

Assess stroke risk based on patient data.

**Headers:**
```
Authorization: Bearer <token>
Content-Type: application/json
```

**Request Body:**
```json
{
  "age": 65,
  "gender": "Male",
  "hypertension": 1,
  "heartDisease": 0,
  "everMarried": "Yes",
  "workType": "Private",
  "residenceType": "Urban",
  "avgGlucoseLevel": 120.5,
  "bmi": 28.3,
  "smokingStatus": "formerly smoked"
}
```

**Field Descriptions:**
- `age`: Number (required) - Patient's age
- `gender`: String (required) - "Male" or "Female"
- `hypertension`: Number (0 or 1) - Has hypertension
- `heartDisease`: Number (0 or 1) - Has heart disease
- `everMarried`: String - "Yes" or "No"
- `workType`: String - "Private", "Self-employed", "Govt_job", "children", "Never_worked"
- `residenceType`: String - "Urban" or "Rural"
- `avgGlucoseLevel`: Number - Average glucose level (mg/dL)
- `bmi`: Number - Body Mass Index
- `smokingStatus`: String - "never smoked", "formerly smoked", "smokes", "Unknown"

**Response:**
```json
{
  "riskLevel": "medium",
  "riskPercentage": 55,
  "recommendations": [
    "💊 راقب ضغط الدم يومياً والتزم بالأدوية الموصوفة",
    "🧂 قلل من تناول الملح والأطعمة المصنعة",
    "🥗 اتبع نظام غذائي صحي غني بالخضروات والفواكه",
    "🏃 مارس الرياضة 30-45 دقيقة يومياً",
    "✅ ممتاز! استمر في الابتعاد عن التدخين"
  ],
  "timestamp": "2024-12-07T19:30:00.000Z"
}
```

**Risk Levels:**
- `low`: Risk percentage < 40%
- `medium`: Risk percentage 40-70%
- `high`: Risk percentage > 70%

---

### 3. Brain Scan Image Analysis
**POST** `/ai/scan-image`

Upload and analyze brain scan images.

**Headers:**
```
Authorization: Bearer <token>
Content-Type: multipart/form-data
```

**Request Body:**
Form data with image file:
```
image: <file> (JPEG, PNG, GIF - max 10MB)
```

**Response:**
```json
{
  "scanId": 1701975000000,
  "result": "normal",
  "confidence": 0.85,
  "findings": [
    "✅ لا توجد علامات واضحة للسكتة الدماغية",
    "الصورة تبدو طبيعية بشكل عام",
    "استمر في المتابعة الدورية مع طبيبك",
    "حافظ على نمط حياة صحي للوقاية"
  ],
  "imageUrl": "/uploads/scans/scan-1701975000000-123456789.jpg",
  "timestamp": "2024-12-07T19:30:00.000Z"
}
```

**Result Types:**
- `normal`: No signs of stroke detected
- `requires_review`: Needs specialist review
- `abnormal`: Potential stroke indicators found

**Confidence:** Float between 0.0 and 1.0 (0% to 100%)

---

## Scans Management

### Get User Scans
**GET** `/scans`

Get all scans for the authenticated user.

**Headers:**
```
Authorization: Bearer <token>
```

**Query Parameters:**
- `limit`: Number (optional) - Max results to return
- `offset`: Number (optional) - Pagination offset

**Response:**
```json
{
  "scans": [
    {
      "id": "scan123",
      "userId": "user123",
      "imageUrl": "/uploads/scans/scan-1701975000000-123456789.jpg",
      "result": "normal",
      "confidence": 0.85,
      "findings": ["..."],
      "createdAt": "2024-12-07T19:30:00.000Z"
    }
  ],
  "total": 1
}
```

### Upload Scan
**POST** `/scans`

Upload a new brain scan (same as `/ai/scan-image` but also saves to database).

---

## FAQs

### Get All FAQs
**GET** `/faqs`

Get frequently asked questions about stroke.

**Response:**
```json
{
  "faqs": [
    {
      "id": "faq1",
      "question": "ما هي السكتة الدماغية؟",
      "answer": "السكتة الدماغية هي حالة طبية طارئة تحدث عندما ينقطع تدفق الدم إلى جزء من الدماغ...",
      "category": "general",
      "order": 1
    }
  ]
}
```

**Categories:**
- `general`: General information
- `symptoms`: Symptoms and signs
- `prevention`: Prevention methods
- `treatment`: Treatment options
- `recovery`: Recovery and rehabilitation

---

## Doctors

### Get All Doctors
**GET** `/doctors`

Get list of available doctors.

**Query Parameters:**
- `specialty`: String (optional) - Filter by specialty
- `city`: String (optional) - Filter by city

**Response:**
```json
{
  "doctors": [
    {
      "id": "doc1",
      "name": "د. أحمد محمود",
      "specialty": "طب الأعصاب",
      "rating": 4.8,
      "reviewsCount": 150,
      "experience": 15,
      "city": "القاهرة",
      "address": "شارع الجمهورية، وسط البلد",
      "phone": "0123456789",
      "imageUrl": "/uploads/doctors/doc1.jpg",
      "availableDays": ["Sunday", "Monday", "Wednesday"],
      "workingHours": "9:00 AM - 5:00 PM"
    }
  ]
}
```

### Get Doctor by ID
**GET** `/doctors/:id`

Get detailed information about a specific doctor.

---

## Bookings

### Get User Bookings
**GET** `/bookings`

Get all bookings for the authenticated user.

**Headers:**
```
Authorization: Bearer <token>
```

**Response:**
```json
{
  "bookings": [
    {
      "id": "booking123",
      "userId": "user123",
      "doctorId": "doc1",
      "doctor": {
        "name": "د. أحمد محمود",
        "specialty": "طب الأعصاب"
      },
      "date": "2024-12-15",
      "time": "10:00 AM",
      "status": "confirmed",
      "notes": "فحص دوري",
      "createdAt": "2024-12-07T19:30:00.000Z"
    }
  ]
}
```

### Create Booking
**POST** `/bookings`

Create a new doctor appointment.

**Headers:**
```
Authorization: Bearer <token>
Content-Type: application/json
```

**Request Body:**
```json
{
  "doctorId": "doc1",
  "date": "2024-12-15",
  "time": "10:00 AM",
  "notes": "فحص دوري"
}
```

**Response:**
```json
{
  "booking": {
    "id": "booking123",
    "userId": "user123",
    "doctorId": "doc1",
    "date": "2024-12-15",
    "time": "10:00 AM",
    "status": "pending",
    "notes": "فحص دوري",
    "createdAt": "2024-12-07T19:30:00.000Z"
  }
}
```

### Cancel Booking
**DELETE** `/bookings/:id`

Cancel a booking.

**Headers:**
```
Authorization: Bearer <token>
```

---

## Favorites

### Get User Favorites
**GET** `/favorites`

Get user's favorite doctors.

**Headers:**
```
Authorization: Bearer <token>
```

**Response:**
```json
{
  "favorites": [
    {
      "id": "fav1",
      "userId": "user123",
      "doctorId": "doc1",
      "doctor": {
        "name": "د. أحمد محمود",
        "specialty": "طب الأعصاب"
      },
      "createdAt": "2024-12-07T19:30:00.000Z"
    }
  ]
}
```

### Add to Favorites
**POST** `/favorites`

Add a doctor to favorites.

**Request Body:**
```json
{
  "doctorId": "doc1"
}
```

### Remove from Favorites
**DELETE** `/favorites/:doctorId`

Remove a doctor from favorites.

---

## Error Responses

All endpoints may return error responses in this format:

```json
{
  "error": {
    "message": "Error description",
    "status": 400
  }
}
```

**Common Status Codes:**
- `400`: Bad Request - Invalid input
- `401`: Unauthorized - Missing or invalid token
- `404`: Not Found - Resource not found
- `500`: Internal Server Error - Server error

---

## Testing the APIs

### Using cURL

**Login:**
```bash
curl -X POST http://localhost:3001/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"ahmed@example.com","password":"password123"}'
```

**Chat:**
```bash
curl -X POST http://localhost:3001/api/ai/chat \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d '{"message":"ما هي أعراض السكتة الدماغية؟"}'
```

**Stroke Assessment:**
```bash
curl -X POST http://localhost:3001/api/ai/stroke-assessment \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d '{"age":65,"gender":"Male","hypertension":1,"heartDisease":0}'
```

**Image Upload:**
```bash
curl -X POST http://localhost:3001/api/ai/scan-image \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -F "image=@brain_scan.jpg"
```

### Using Postman

1. Import the API endpoints
2. Set up environment variables for base URL and token
3. Use the examples above as request templates

---

## Rate Limiting

Currently no rate limiting is implemented. For production, consider adding rate limiting to prevent abuse.

---

## Support

For issues or questions, contact the development team.
