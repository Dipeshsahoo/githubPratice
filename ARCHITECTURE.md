# Alumni Website - System Architecture

## Overview
Production-ready Alumni Website for a school's Platinum Jubilee celebration. Built with React frontend, Flask backend, PostgreSQL database, and JWT authentication.

## Tech Stack

### Frontend
- **React 18+** - UI framework
- **Tailwind CSS** - Styling
- **React Router** - Navigation
- **Axios** - HTTP client
- **React Query** - Data fetching & caching
- **JWT Decode** - Token management

### Backend
- **Flask** - Web framework
- **Flask-SQLAlchemy** - ORM
- **Flask-JWT-Extended** - JWT authentication
- **Flask-CORS** - CORS handling
- **Flask-Migrate** - Database migrations
- **psycopg2** - PostgreSQL adapter
- **Pillow** - Image processing
- **python-dotenv** - Environment variables
- **bcrypt** - Password hashing

### Database
- **PostgreSQL** - Primary database

### AI Chatbot
- **OpenAI API** or **LangChain** - LLM integration
- **Vector Database** (FAISS/Chroma) - Knowledge base embeddings
- **Retrieval-Augmented Generation (RAG)** - Context-aware responses

## System Architecture

```
┌─────────────────┐
│   React Client  │
│  (Frontend)     │
└────────┬────────┘
         │ HTTPS/REST API
         │
┌────────▼────────┐
│  Flask Backend  │
│   (REST API)    │
└────────┬────────┘
         │
    ┌────┴────┐
    │         │
┌───▼───┐ ┌──▼──────┐
│PostgreSQL│ │File Storage│
│Database │ │  (uploads)  │
└─────────┘ └────────────┘
```

## Module Architecture

### 1. Authentication Module
- JWT token-based authentication
- Email/mobile verification
- Role-based access (Admin, Alumni, Visitor)
- Password reset functionality

### 2. Alumni Directory Module
- Search & filter functionality
- Public/private profile visibility
- Contact information management

### 3. Events & Jubilee Module
- Event CRUD operations
- Registration system
- QR code generation for check-in
- Countdown timer for Platinum Jubilee

### 4. News & Announcements Module
- Admin-posted announcements
- Share functionality
- Categorization

### 5. Gallery & Media Module
- Image/video upload
- Album management
- Event-based organization

### 6. Mentorship & Jobs Module
- Posting system
- Application tracking
- Search & filter

### 7. Donations Module
- Donation form
- Status tracking
- Admin approval workflow

### 8. Admin Dashboard
- User management
- Content moderation
- Analytics & statistics
- Event management

### 9. AI Chatbot Module
- Knowledge base from website content
- RAG-based responses
- Context-aware conversations
- Widget UI integration

## API Structure

### Base URL
```
/api/v1
```

### Endpoints by Module

#### Authentication
- `POST /auth/register` - Alumni registration
- `POST /auth/login` - User login
- `POST /auth/verify` - Email/mobile verification
- `POST /auth/refresh` - Token refresh
- `POST /auth/logout` - Logout
- `POST /auth/forgot-password` - Password reset request
- `POST /auth/reset-password` - Password reset

#### Alumni
- `GET /alumni` - List alumni (with filters)
- `GET /alumni/:id` - Get alumni profile
- `PUT /alumni/:id` - Update profile
- `POST /alumni/:id/complete-profile` - Complete profile

#### Events
- `GET /events` - List events
- `GET /events/:id` - Get event details
- `POST /events` - Create event (admin)
- `PUT /events/:id` - Update event (admin)
- `DELETE /events/:id` - Delete event (admin)
- `POST /events/:id/register` - Register for event
- `POST /events/:id/checkin` - QR check-in

#### News
- `GET /news` - List announcements
- `GET /news/:id` - Get announcement
- `POST /news` - Create announcement (admin)
- `PUT /news/:id` - Update announcement (admin)
- `DELETE /news/:id` - Delete announcement (admin)

#### Gallery
- `GET /gallery` - List albums
- `GET /gallery/:id` - Get album
- `POST /gallery` - Create album (admin)
- `POST /gallery/:id/upload` - Upload media
- `DELETE /gallery/:id` - Delete album (admin)

#### Mentorship
- `GET /mentorship` - List mentorship posts
- `POST /mentorship` - Create mentorship post
- `PUT /mentorship/:id` - Update post
- `DELETE /mentorship/:id` - Delete post

#### Jobs
- `GET /jobs` - List job postings
- `POST /jobs` - Create job posting
- `PUT /jobs/:id` - Update posting
- `DELETE /jobs/:id` - Delete posting
- `POST /jobs/:id/apply` - Apply for job

#### Donations
- `GET /donations` - List donations (admin)
- `POST /donations` - Create donation
- `PUT /donations/:id` - Update donation status (admin)

#### Admin
- `GET /admin/stats` - Dashboard statistics
- `GET /admin/users` - List users
- `PUT /admin/users/:id/approve` - Approve user
- `PUT /admin/users/:id/role` - Change user role

#### Chatbot
- `POST /chatbot/query` - Chatbot query
- `POST /chatbot/query-whatsapp` - WhatsApp API endpoint

## Security

1. **JWT Tokens**
   - Access tokens (short-lived)
   - Refresh tokens (long-lived)
   - Secure cookie storage option

2. **Password Security**
   - bcrypt hashing
   - Minimum complexity requirements

3. **Input Validation**
   - Server-side validation
   - SQL injection prevention (ORM)
   - XSS prevention

4. **File Upload Security**
   - File type validation
   - Size limits
   - Virus scanning (optional)

5. **CORS**
   - Configured for specific origins
   - Credentials support

## Deployment Considerations

- Environment variables for sensitive data
- Database connection pooling
- Static file serving (Nginx)
- SSL/TLS certificates
- Rate limiting
- Logging & monitoring
- Backup strategy
