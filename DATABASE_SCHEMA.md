# Database Schema

## Tables Overview

### Core Tables
1. `users` - User accounts (alumni, admin)
2. `profiles` - Extended user profiles
3. `events` - Event information
4. `event_registrations` - Event registration records
5. `news` - News and announcements
6. `albums` - Photo/video albums
7. `media` - Media files
8. `mentorship_posts` - Mentorship availability posts
9. `job_postings` - Job/internship postings
10. `job_applications` - Job applications
11. `donations` - Donation records
12. `chatbot_knowledge` - Chatbot knowledge base entries

## Detailed Schema

### users
```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    mobile VARCHAR(20) UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    role VARCHAR(20) DEFAULT 'alumni' CHECK (role IN ('admin', 'alumni', 'visitor')),
    is_verified BOOLEAN DEFAULT FALSE,
    is_approved BOOLEAN DEFAULT FALSE,
    verification_token VARCHAR(255),
    reset_token VARCHAR(255),
    reset_token_expires TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_login TIMESTAMP
);
```

### profiles
```sql
CREATE TABLE profiles (
    id SERIAL PRIMARY KEY,
    user_id INTEGER UNIQUE NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    batch_year INTEGER,
    profession VARCHAR(255),
    company VARCHAR(255),
    location VARCHAR(255),
    bio TEXT,
    profile_picture VARCHAR(255),
    linkedin_url VARCHAR(255),
    website_url VARCHAR(255),
    is_profile_complete BOOLEAN DEFAULT FALSE,
    show_contact_info BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### events
```sql
CREATE TABLE events (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    event_type VARCHAR(50) CHECK (event_type IN ('jubilee', 'reunion', 'workshop', 'other')),
    start_date TIMESTAMP NOT NULL,
    end_date TIMESTAMP,
    location VARCHAR(255),
    venue VARCHAR(255),
    max_participants INTEGER,
    registration_deadline TIMESTAMP,
    is_jubilee_event BOOLEAN DEFAULT FALSE,
    created_by INTEGER REFERENCES users(id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### event_registrations
```sql
CREATE TABLE event_registrations (
    id SERIAL PRIMARY KEY,
    event_id INTEGER NOT NULL REFERENCES events(id) ON DELETE CASCADE,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    qr_code VARCHAR(255) UNIQUE,
    check_in_time TIMESTAMP,
    is_checked_in BOOLEAN DEFAULT FALSE,
    registration_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(event_id, user_id)
);
```

### news
```sql
CREATE TABLE news (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    content TEXT NOT NULL,
    category VARCHAR(50),
    author_id INTEGER REFERENCES users(id),
    is_published BOOLEAN DEFAULT FALSE,
    published_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### albums
```sql
CREATE TABLE albums (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    event_id INTEGER REFERENCES events(id),
    created_by INTEGER REFERENCES users(id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### media
```sql
CREATE TABLE media (
    id SERIAL PRIMARY KEY,
    album_id INTEGER NOT NULL REFERENCES albums(id) ON DELETE CASCADE,
    file_path VARCHAR(255) NOT NULL,
    file_type VARCHAR(50) NOT NULL CHECK (file_type IN ('image', 'video')),
    file_size INTEGER,
    thumbnail_path VARCHAR(255),
    uploaded_by INTEGER REFERENCES users(id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### mentorship_posts
```sql
CREATE TABLE mentorship_posts (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    title VARCHAR(255) NOT NULL,
    description TEXT NOT NULL,
    expertise_area VARCHAR(255),
    availability_status VARCHAR(20) DEFAULT 'available' CHECK (availability_status IN ('available', 'limited', 'unavailable')),
    is_approved BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### job_postings
```sql
CREATE TABLE job_postings (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    title VARCHAR(255) NOT NULL,
    company VARCHAR(255) NOT NULL,
    description TEXT NOT NULL,
    location VARCHAR(255),
    job_type VARCHAR(50) CHECK (job_type IN ('full-time', 'part-time', 'internship', 'contract')),
    application_deadline TIMESTAMP,
    application_link VARCHAR(255),
    is_approved BOOLEAN DEFAULT FALSE,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### job_applications
```sql
CREATE TABLE job_applications (
    id SERIAL PRIMARY KEY,
    job_posting_id INTEGER NOT NULL REFERENCES job_postings(id) ON DELETE CASCADE,
    applicant_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    resume_path VARCHAR(255),
    cover_letter TEXT,
    status VARCHAR(20) DEFAULT 'pending' CHECK (status IN ('pending', 'reviewed', 'shortlisted', 'rejected', 'accepted')),
    applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(job_posting_id, applicant_id)
);
```

### donations
```sql
CREATE TABLE donations (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    donor_name VARCHAR(255) NOT NULL,
    donor_email VARCHAR(255),
    donor_mobile VARCHAR(20),
    amount DECIMAL(10, 2) NOT NULL,
    purpose VARCHAR(255),
    status VARCHAR(20) DEFAULT 'pending' CHECK (status IN ('pending', 'approved', 'rejected', 'completed')),
    payment_method VARCHAR(50),
    transaction_id VARCHAR(255),
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### chatbot_knowledge
```sql
CREATE TABLE chatbot_knowledge (
    id SERIAL PRIMARY KEY,
    category VARCHAR(100) NOT NULL,
    question TEXT NOT NULL,
    answer TEXT NOT NULL,
    source_type VARCHAR(50) CHECK (source_type IN ('static', 'database', 'event', 'faq')),
    source_id INTEGER,
    embedding VECTOR(1536), -- For OpenAI embeddings
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create index for vector similarity search
CREATE INDEX ON chatbot_knowledge USING ivfflat (embedding vector_cosine_ops);
```

## Indexes

```sql
-- Performance indexes
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_mobile ON users(mobile);
CREATE INDEX idx_profiles_user_id ON profiles(user_id);
CREATE INDEX idx_profiles_batch_year ON profiles(batch_year);
CREATE INDEX idx_profiles_profession ON profiles(profession);
CREATE INDEX idx_profiles_location ON profiles(location);
CREATE INDEX idx_events_start_date ON events(start_date);
CREATE INDEX idx_events_event_type ON events(event_type);
CREATE INDEX idx_event_registrations_event_id ON event_registrations(event_id);
CREATE INDEX idx_event_registrations_user_id ON event_registrations(user_id);
CREATE INDEX idx_event_registrations_qr_code ON event_registrations(qr_code);
CREATE INDEX idx_news_published_at ON news(published_at);
CREATE INDEX idx_media_album_id ON media(album_id);
CREATE INDEX idx_job_postings_is_active ON job_postings(is_active);
CREATE INDEX idx_chatbot_knowledge_category ON chatbot_knowledge(category);
```

## Relationships

- `users` 1:1 `profiles`
- `users` 1:N `events` (created_by)
- `users` 1:N `event_registrations`
- `events` 1:N `event_registrations`
- `events` 1:N `albums`
- `albums` 1:N `media`
- `users` 1:N `mentorship_posts`
- `users` 1:N `job_postings`
- `users` 1:N `job_applications` (applicant)
- `job_postings` 1:N `job_applications`
- `users` 1:N `donations`
