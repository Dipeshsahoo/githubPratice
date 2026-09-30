"""
Script to help identify SQLAlchemy patterns that need to be converted to MongoDB
Run this to see what needs to be changed in route files
"""

import re
import os

# Patterns to find and replace
patterns = [
    (r'from extensions import db', r''),
    (r'\.query\.filter_by\(([^)]+)\)', r'.objects(\1)'),
    (r'\.query\.get\(([^)]+)\)', r'.objects(id=\1).first()'),
    (r'\.query\.filter\(([^)]+)\)', r'.objects(\1)'),
    (r'db\.session\.add\(([^)]+)\)', r'\1.save()'),
    (r'db\.session\.commit\(\)', r''),
    (r'db\.session\.delete\(([^)]+)\)', r'\1.delete()'),
    (r'\.paginate\(([^)]+)\)', r'.skip().limit()'),  # Needs manual conversion
]

def find_patterns_in_file(filepath):
    """Find SQLAlchemy patterns in a file"""
    with open(filepath, 'r') as f:
        content = f.read()
    
    issues = []
    if 'from extensions import db' in content:
        issues.append("Remove 'from extensions import db'")
    if '.query.' in content:
        issues.append("Convert .query. to .objects")
    if 'db.session.add' in content:
        issues.append("Replace db.session.add() with .save()")
    if 'db.session.commit' in content:
        issues.append("Remove db.session.commit()")
    if 'db.session.delete' in content:
        issues.append("Replace db.session.delete() with .delete()")
    
    return issues

# Check all route files
routes_dir = 'routes'
if os.path.exists(routes_dir):
    for filename in os.listdir(routes_dir):
        if filename.endswith('.py') and filename != '__init__.py':
            filepath = os.path.join(routes_dir, filename)
            issues = find_patterns_in_file(filepath)
            if issues:
                print(f"\n{filename}:")
                for issue in issues:
                    print(f"  - {issue}")

print("\nNote: This script only identifies issues. Manual conversion is required.")
print("See MONGODB_MIGRATION.md for conversion patterns.")
