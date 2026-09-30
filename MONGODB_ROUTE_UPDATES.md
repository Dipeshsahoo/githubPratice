# MongoDB Route Updates - Quick Reference

## Common Replacements

### 1. Remove db imports
```python
# Remove this line:
from extensions import db
```

### 2. Query replacements
```python
# OLD:
User.query.filter_by(email=email).first()
User.query.get(user_id)
User.query.filter(User.role == 'alumni').all()

# NEW:
User.objects(email=email).first()
User.objects(id=user_id).first()
User.objects(role='alumni')
```

### 3. Save operations
```python
# OLD:
db.session.add(user)
db.session.commit()

# NEW:
user.save()  # Auto-commits in MongoDB
```

### 4. Delete operations
```python
# OLD:
db.session.delete(user)
db.session.commit()

# NEW:
user.delete()
```

### 5. Pagination
```python
# OLD:
query.paginate(page=page, per_page=per_page)

# NEW:
skip = (page - 1) * per_page
items = query.skip(skip).limit(per_page)
total = query.count()
pages = (total + per_page - 1) // per_page
```

### 6. ID handling
```python
# OLD:
user_id = user.id  # Integer

# NEW:
user_id = str(user.id)  # String (ObjectId)
```

### 7. Complex queries
```python
# OLD:
from sqlalchemy import or_
query.filter(or_(Profile.first_name.ilike(...), Profile.last_name.ilike(...)))

# NEW:
from mongoengine import Q
query.filter(Q(first_name__icontains=...) | Q(last_name__icontains=...))
```

### 8. Aggregations
```python
# OLD:
db.session.query(func.sum(Donation.amount)).scalar()

# NEW:
from mongoengine.queryset.visitor import Q
pipeline = [{"$group": {"_id": None, "total": {"$sum": "$amount"}}}]
result = Donation.objects.aggregate(*pipeline)
total = next(result, {}).get('total', 0)
```

## Status

✅ Updated: auth.py
⏳ Remaining: alumni.py, events.py, news.py, gallery.py, mentorship.py, jobs.py, donations.py, admin.py, chatbot.py

## Next Steps

1. Update each route file using the patterns above
2. Test each endpoint after updating
3. Update init_db.py to use MongoDB
4. Update any utility functions that use db
