# MongoDB Migration Guide

## Changes Made

### 1. Dependencies
- Removed: `Flask-SQLAlchemy`, `Flask-Migrate`, `psycopg2-binary`
- Added: `mongoengine`, `pymongo`

### 2. Configuration
- Changed from `SQLALCHEMY_DATABASE_URI` to `MONGODB_URI` or individual MongoDB settings
- Default connection: `mongodb://localhost:27017/alumni_db`

### 3. Models
All models converted from SQLAlchemy to MongoEngine:
- `db.Model` → `Document`
- `db.Column()` → `fields.FieldType()`
- `__tablename__` → `meta = {'collection': 'name'}`
- Integer IDs → String IDs (MongoDB ObjectIds)

### 4. Query Patterns

#### Old (SQLAlchemy):
```python
User.query.filter_by(email=email).first()
User.query.get(user_id)
User.query.filter(User.role == 'alumni').all()
db.session.add(user)
db.session.commit()
db.session.delete(user)
```

#### New (MongoDB):
```python
User.objects(email=email).first()
User.objects(id=user_id).first()
User.objects(role='alumni')
user.save()  # Auto-commits
user.delete()
```

### 5. ID Handling
- All IDs are now strings (ObjectId strings)
- Use `str(model.id)` when returning IDs
- When querying, IDs are automatically converted

### 6. Relationships
- No foreign keys in MongoDB
- Use string references: `user_id = fields.StringField()`
- Manual joins using `.objects(id=user_id).first()`

## Route Updates Needed

All routes need to be updated from SQLAlchemy to MongoDB queries. Key changes:

1. Remove `from extensions import db`
2. Change `Model.query.*` to `Model.objects.*`
3. Remove `db.session.add()` and `db.session.commit()`
4. Use `.save()` instead
5. Convert integer IDs to strings where needed

## Environment Variables

Update `.env` file:
```env
MONGODB_URI=mongodb://localhost:27017/alumni_db
# OR
MONGODB_HOST=localhost
MONGODB_PORT=27017
MONGODB_DB=alumni_db
MONGODB_USERNAME=  # Optional
MONGODB_PASSWORD=  # Optional
```

## Next Steps

1. Install new dependencies: `pip install -r requirements.txt`
2. Start MongoDB server
3. Update all route files to use MongoDB queries
4. Test all endpoints
