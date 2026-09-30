# Database Setup Guide

## Current Error
```
psycopg2.OperationalError: connection to server at "localhost" (::1), port 5432 failed: Connection refused
```

This means PostgreSQL is not running or not accessible.

## Solution Options

### Option 1: Start PostgreSQL (Recommended for Production)

#### Windows:
1. **Check if PostgreSQL is installed:**
   ```powershell
   Get-Service -Name postgresql*
   ```

2. **Start PostgreSQL service:**
   ```powershell
   Start-Service postgresql-x64-XX  # Replace XX with your version
   ```
   
   Or use Services app:
   - Press `Win + R`, type `services.msc`
   - Find "PostgreSQL" service
   - Right-click → Start

3. **Create database:**
   ```powershell
   psql -U postgres
   ```
   Then in psql:
   ```sql
   CREATE DATABASE alumni_db;
   \q
   ```

4. **Update .env file:**
   ```
   DATABASE_URL=postgresql://postgres:YOUR_PASSWORD@localhost:5432/alumni_db
   ```

#### Mac/Linux:
```bash
# Start PostgreSQL
sudo service postgresql start
# or
brew services start postgresql

# Create database
psql -U postgres
CREATE DATABASE alumni_db;
\q
```

### Option 2: Use SQLite for Quick Development (Easier)

If you want to get started quickly without PostgreSQL:

1. **Update `backend/config.py`** to use SQLite by default:
   ```python
   SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///alumni.db'
   ```

2. **Or update your `.env` file:**
   ```
   DATABASE_URL=sqlite:///alumni.db
   ```

3. **No need to start any database server!**

**Note:** SQLite is fine for development, but PostgreSQL is recommended for production.

### Option 3: Install PostgreSQL (If Not Installed)

#### Windows:
1. Download from: https://www.postgresql.org/download/windows/
2. Run installer
3. Remember the password you set for `postgres` user
4. Start the service (see Option 1)

#### Mac:
```bash
brew install postgresql
brew services start postgresql
```

#### Linux (Ubuntu/Debian):
```bash
sudo apt-get update
sudo apt-get install postgresql postgresql-contrib
sudo systemctl start postgresql
```

## Verify Database Connection

After setting up, test the connection:

```powershell
cd backend
python -c "from app import create_app; from extensions import db; app = create_app(); app.app_context().push(); db.engine.connect(); print('✓ Database connection successful!')"
```

## Quick Start (SQLite)

If you just want to get the app running quickly:

1. **Update `.env` in backend folder:**
   ```
   DATABASE_URL=sqlite:///alumni.db
   ```

2. **Start the server:**
   ```powershell
   python app.py
   ```

3. **Database file will be created automatically** at `backend/alumni.db`

## Troubleshooting

### "Connection refused" error:
- PostgreSQL service is not running
- Wrong port (default is 5432)
- Firewall blocking connection

### "Authentication failed" error:
- Wrong password in DATABASE_URL
- User doesn't exist

### "Database does not exist" error:
- Run: `CREATE DATABASE alumni_db;` in psql

## Recommended Setup for Development

For quick development, use SQLite:
```
DATABASE_URL=sqlite:///alumni.db
```

For production, use PostgreSQL:
```
DATABASE_URL=postgresql://username:password@localhost:5432/alumni_db
```
