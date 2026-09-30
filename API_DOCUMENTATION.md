# API Documentation

Base URL: `http://localhost:5000/api/v1`

## Authentication

Most endpoints require JWT authentication. Include the token in the Authorization header:
```
Authorization: Bearer <access_token>
```

---

## Auth Endpoints

### Register
**POST** `/auth/register`

Register a new alumni account.

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "password123",
  "mobile": "+1234567890",
  "first_name": "John",
  "last_name": "Doe"
}
```

**Response:** `201 Created`
```json
{
  "message": "Registration successful. Please verify your email/mobile.",
  "user_id": 1,
  "verification_token": "token_string"
}
```

### Login
**POST** `/auth/login`

Login and get access tokens.

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "password123"
}
```

**Response:** `200 OK`
```json
{
  "access_token": "jwt_token",
  "refresh_token": "refresh_token",
  "user": { ... }
}
```

### Verify
**POST** `/auth/verify`

Verify email/mobile with token.

**Request Body:**
```json
{
  "user_id": 1,
  "token": "verification_token"
}
```

### Refresh Token
**POST** `/auth/refresh`

Refresh access token using refresh token.

**Headers:** `Authorization: Bearer <refresh_token>`

**Response:** `200 OK`
```json
{
  "access_token": "new_jwt_token"
}
```

### Forgot Password
**POST** `/auth/forgot-password`

Request password reset.

**Request Body:**
```json
{
  "email": "user@example.com"
}
```

### Reset Password
**POST** `/auth/reset-password`

Reset password with token.

**Request Body:**
```json
{
  "token": "reset_token",
  "password": "new_password"
}
```

---

## Alumni Endpoints

### List Alumni
**GET** `/alumni`

Get paginated list of alumni with filters.

**Query Parameters:**
- `search`: Search term (name, profession, company)
- `batch_year`: Filter by batch year
- `profession`: Filter by profession
- `location`: Filter by location
- `page`: Page number (default: 1)
- `per_page`: Items per page (default: 20)

**Response:** `200 OK`
```json
{
  "alumni": [...],
  "total": 100,
  "page": 1,
  "per_page": 20,
  "pages": 5
}
```

### Get Alumni Profile
**GET** `/alumni/:id`

Get specific alumni profile.

**Response:** `200 OK`
```json
{
  "user": { ... },
  "profile": { ... }
}
```

### Update Profile
**PUT** `/alumni/:id`

Update alumni profile. Requires authentication.

**Request Body:**
```json
{
  "first_name": "John",
  "last_name": "Doe",
  "batch_year": 2020,
  "profession": "Engineer",
  "company": "Tech Corp",
  "location": "Mumbai",
  "bio": "Bio text",
  "linkedin_url": "https://linkedin.com/in/johndoe",
  "website_url": "https://johndoe.com"
}
```

### Complete Profile
**POST** `/alumni/:id/complete-profile`

Complete profile after first login. Requires authentication.

**Request Body:**
```json
{
  "first_name": "John",
  "last_name": "Doe",
  "batch_year": 2020,
  "profession": "Engineer",
  "company": "Tech Corp",
  "location": "Mumbai"
}
```

---

## Events Endpoints

### List Events
**GET** `/events`

Get paginated list of events.

**Query Parameters:**
- `type`: Event type (jubilee, reunion, workshop, other)
- `is_jubilee`: Filter jubilee events (true/false)
- `page`: Page number
- `per_page`: Items per page

**Response:** `200 OK`
```json
{
  "events": [...],
  "total": 50,
  "page": 1,
  "per_page": 20,
  "pages": 3
}
```

### Get Event
**GET** `/events/:id`

Get event details.

**Response:** `200 OK`
```json
{
  "id": 1,
  "title": "Platinum Jubilee Celebration",
  "description": "...",
  "start_date": "2024-12-31T00:00:00",
  "location": "School Campus",
  "is_registered": false,
  "registration": null
}
```

### Create Event
**POST** `/events`

Create new event. **Admin only.**

**Request Body:**
```json
{
  "title": "Event Title",
  "description": "Event description",
  "event_type": "jubilee",
  "start_date": "2024-12-31T00:00:00",
  "end_date": "2024-12-31T23:59:59",
  "location": "Venue",
  "venue": "Hall Name",
  "max_participants": 100,
  "registration_deadline": "2024-12-25T00:00:00",
  "is_jubilee_event": true
}
```

### Update Event
**PUT** `/events/:id`

Update event. **Admin only.**

### Delete Event
**DELETE** `/events/:id`

Delete event. **Admin only.**

### Register for Event
**POST** `/events/:id/register`

Register for an event. **Alumni only.**

**Response:** `201 Created`
```json
{
  "message": "Registered successfully",
  "registration": { ... },
  "qr_code_image": "data:image/png;base64,..."
}
```

### Check-in
**POST** `/events/:id/checkin`

QR code check-in. **Admin only.**

**Request Body:**
```json
{
  "qr_code": "event_1_user_1_abc123"
}
```

---

## News Endpoints

### List News
**GET** `/news`

Get paginated list of news articles.

**Query Parameters:**
- `category`: Filter by category
- `published_only`: Only published (true/false, default: true)
- `page`: Page number
- `per_page`: Items per page

### Get News Article
**GET** `/news/:id`

Get specific news article.

### Create News
**POST** `/news`

Create news article. **Admin only.**

**Request Body:**
```json
{
  "title": "News Title",
  "content": "News content...",
  "category": "Announcement",
  "is_published": true
}
```

### Update News
**PUT** `/news/:id`

Update news article. **Admin only.**

### Delete News
**DELETE** `/news/:id`

Delete news article. **Admin only.**

---

## Gallery Endpoints

### List Albums
**GET** `/gallery`

Get paginated list of albums.

**Query Parameters:**
- `event_id`: Filter by event
- `page`: Page number
- `per_page`: Items per page

### Get Album
**GET** `/gallery/:id`

Get album with media files.

### Create Album
**POST** `/gallery`

Create album. **Admin only.**

**Request Body:**
```json
{
  "title": "Album Title",
  "description": "Album description",
  "event_id": 1
}
```

### Upload Media
**POST** `/gallery/:id/upload`

Upload media to album. **Admin only.**

**Request:** `multipart/form-data`
- `file`: Media file (image/video)

### Delete Album
**DELETE** `/gallery/:id`

Delete album. **Admin only.**

---

## Mentorship Endpoints

### List Mentorship Posts
**GET** `/mentorship`

Get paginated list of mentorship posts.

**Query Parameters:**
- `expertise`: Filter by expertise area
- `availability`: Filter by availability status
- `approved_only`: Only approved (true/false, default: true)
- `page`: Page number
- `per_page`: Items per page

### Get Mentorship Post
**GET** `/mentorship/:id`

Get specific mentorship post.

### Create Mentorship Post
**POST** `/mentorship`

Create mentorship post. **Alumni only.**

**Request Body:**
```json
{
  "title": "Mentorship Title",
  "description": "Description...",
  "expertise_area": "Software Engineering",
  "availability_status": "available"
}
```

### Update Mentorship Post
**PUT** `/mentorship/:id`

Update mentorship post. **Owner or Admin.**

### Delete Mentorship Post
**DELETE** `/mentorship/:id`

Delete mentorship post. **Owner or Admin.**

### Approve Mentorship Post
**POST** `/mentorship/:id/approve`

Approve mentorship post. **Admin only.**

---

## Jobs Endpoints

### List Jobs
**GET** `/jobs`

Get paginated list of job postings.

**Query Parameters:**
- `job_type`: Filter by job type
- `location`: Filter by location
- `active_only`: Only active (true/false, default: true)
- `approved_only`: Only approved (true/false, default: true)
- `page`: Page number
- `per_page`: Items per page

### Get Job
**GET** `/jobs/:id`

Get specific job posting.

### Create Job Posting
**POST** `/jobs`

Create job posting. **Alumni only.**

**Request Body:**
```json
{
  "title": "Software Engineer",
  "company": "Tech Corp",
  "description": "Job description...",
  "location": "Mumbai",
  "job_type": "full-time",
  "application_deadline": "2024-12-31T00:00:00",
  "application_link": "https://apply.com"
}
```

### Update Job Posting
**PUT** `/jobs/:id`

Update job posting. **Owner or Admin.**

### Delete Job Posting
**DELETE** `/jobs/:id`

Delete job posting. **Owner or Admin.**

### Apply for Job
**POST** `/jobs/:id/apply`

Apply for a job. **Alumni only.**

**Request:** `multipart/form-data` or JSON
```json
{
  "cover_letter": "Cover letter text..."
}
```
- `resume`: Resume file (optional)
- `cover_letter`: Cover letter text

### Approve Job Posting
**POST** `/jobs/:id/approve`

Approve job posting. **Admin only.**

---

## Donations Endpoints

### List Donations
**GET** `/donations`

Get paginated list of donations. **Admin only.**

**Query Parameters:**
- `status`: Filter by status
- `page`: Page number
- `per_page`: Items per page

**Response:** `200 OK`
```json
{
  "donations": [...],
  "total": 50,
  "total_amount": 50000.00,
  ...
}
```

### Create Donation
**POST** `/donations`

Create donation record. **Public.**

**Request Body:**
```json
{
  "donor_name": "John Doe",
  "donor_email": "john@example.com",
  "donor_mobile": "+1234567890",
  "amount": 1000.00,
  "purpose": "School Development",
  "payment_method": "bank_transfer"
}
```

### Update Donation
**PUT** `/donations/:id`

Update donation status. **Admin only.**

**Request Body:**
```json
{
  "status": "approved",
  "payment_method": "bank_transfer",
  "transaction_id": "TXN123456",
  "notes": "Payment received"
}
```

---

## Admin Endpoints

### Get Statistics
**GET** `/admin/stats`

Get dashboard statistics. **Admin only.**

**Response:** `200 OK`
```json
{
  "users": {
    "total": 500,
    "alumni": 480,
    "approved": 450,
    "pending_approval": 30
  },
  "events": {
    "total": 20,
    "upcoming": 5,
    "jubilee_events": 3
  },
  "news": { ... },
  "mentorship": { ... },
  "jobs": { ... },
  "donations": { ... }
}
```

### List Users
**GET** `/admin/users`

List all users. **Admin only.**

**Query Parameters:**
- `role`: Filter by role
- `is_approved`: Filter by approval status
- `page`: Page number
- `per_page`: Items per page

### Approve User
**PUT** `/admin/users/:id/approve`

Approve user account. **Admin only.**

### Change User Role
**PUT** `/admin/users/:id/role`

Change user role. **Admin only.**

**Request Body:**
```json
{
  "role": "admin"
}
```

---

## Chatbot Endpoints

### Query Chatbot
**POST** `/chatbot/query`

Query the AI chatbot.

**Request Body:**
```json
{
  "query": "How do I register for events?"
}
```

**Response:** `200 OK`
```json
{
  "response": "To register for events...",
  "sources": ["website_data", "knowledge_base"]
}
```

### WhatsApp Query
**POST** `/chatbot/query-whatsapp`

WhatsApp API endpoint for chatbot.

**Request Body:**
```json
{
  "query": "How do I register?",
  "phone_number": "+1234567890"
}
```

**Response:** `200 OK`
```json
{
  "message": "To register...",
  "phone_number": "+1234567890"
}
```

### Add Knowledge Entry
**POST** `/chatbot/knowledge`

Add knowledge base entry. **Admin only.**

**Request Body:**
```json
{
  "category": "registration",
  "question": "How to register?",
  "answer": "Go to register page...",
  "source_type": "static",
  "source_id": null
}
```

### List Knowledge Entries
**GET** `/chatbot/knowledge`

List knowledge base entries. **Admin only.**

---

## Error Responses

All endpoints may return error responses:

**400 Bad Request**
```json
{
  "error": "Error message"
}
```

**401 Unauthorized**
```json
{
  "error": "Authentication required"
}
```

**403 Forbidden**
```json
{
  "error": "Permission denied"
}
```

**404 Not Found**
```json
{
  "error": "Resource not found"
}
```

**500 Internal Server Error**
```json
{
  "error": "Internal server error",
  "message": "Detailed error message"
}
```

---

## Rate Limiting

API rate limiting may be implemented in production. Check response headers for rate limit information.

## Pagination

Paginated endpoints return:
- `total`: Total number of items
- `page`: Current page number
- `per_page`: Items per page
- `pages`: Total number of pages

## File Uploads

File upload endpoints accept:
- Images: jpg, jpeg, png, gif
- Videos: mp4, avi, mov
- Documents: pdf, doc, docx

Maximum file size: 10MB (configurable)
