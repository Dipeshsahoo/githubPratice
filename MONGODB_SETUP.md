# MongoDB Setup Guide

## ✅ Conversion Complete

The project has been converted from PostgreSQL/SQLAlchemy to MongoDB/MongoEngine.

## What Changed

1. **Dependencies**: Replaced SQLAlchemy with MongoEngine
2. **Models**: All models converted to MongoDB Documents
3. **Configuration**: Updated to use MongoDB connection strings
4. **Routes**: Partially updated (auth.py and alumni.py complete)

## Setup Instructions

### 1. Install MongoDB

**Windows:**
- Download from: https://www.mongodb.com/try/download/community
- Install and start MongoDB service

**Mac:**
```bash
brew install mongodb-community
brew services start mongodb-community
```

**Linux:**
```bash
sudo apt-get install mongodb
sudo systemctl start mongodb
```

### 2. Install Python Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### 3. Configure Environment

Create/update `backend/.env`:
```env
MONGODB_URI=mongodb://localhost:27017/alumni_db
# OR use individual settings:
MONGODB_HOST=localhost
MONGODB_PORT=27017
MONGODB_DB=alumni_db
MONGODB_USERNAME=  # Optional
MONGODB_PASSWORD=  # Optional

SECRET_KEY=your-secret-key
JWT_SECRET_KEY=your-jwt-secret-key
OPENAI_API_KEY=  # Optional
CORS_ORIGINS=http://localhost:3000,http://localhost:5173
```

### 4. Start MongoDB

Make sure MongoDB is running:
```bash
# Check if running
mongosh  # Should connect successfully
```

### 5. Initialize Database

```bash
cd backend
python init_db.py
python init_db.py create_admin admin@example.com admin123
```

### 6. Start Backend

```bash
python app.py
```

## Remaining Route Updates

The following route files still need MongoDB conversion:
- events.py
- news.py
- gallery.py
- mentorship.py
- jobs.py
- donations.py
- admin.py
- chatbot.py

See `MONGODB_ROUTE_UPDATES.md` for conversion patterns.

## Key Differences from PostgreSQL

1. **No Migrations**: MongoDB is schema-less
2. **String IDs**: All IDs are now strings (ObjectIds)
3. **No Foreign Keys**: Use string references
4. **Different Queries**: `.objects()` instead of `.query`
5. **Auto-commit**: `.save()` auto-commits, no need for `db.session.commit()`

## Testing

After setup, test the API:
```bash
# Health check
curl http://localhost:5000/

# Register user
curl -X POST http://localhost:5000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"test123"}'
```

## Troubleshooting

### MongoDB Connection Error
- Ensure MongoDB is running: `mongosh`
- Check connection string in `.env`
- Verify MongoDB port (default: 27017)

### Import Errors
- Reinstall dependencies: `pip install -r requirements.txt`
- Ensure virtual environment is activated

### Route Errors
- Some routes may still have SQLAlchemy code
- See `MONGODB_CONVERSION_STATUS.md` for status
- Update remaining routes using patterns in `MONGODB_ROUTE_UPDATES.md`
