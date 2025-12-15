import json
import os
from datetime import datetime

# Point to the backend/data directory (one level up from flask_server)
DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'data')

def load_json_file(filename):
    """Load JSON file from data directory"""
    filepath = os.path.join(DATA_DIR, filename)
    if not os.path.exists(filepath):
        return [] if filename != 'db.json' else {}
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        return [] if filename != 'db.json' else {}

def save_json_file(filename, data):
    """Save data to JSON file"""
    os.makedirs(DATA_DIR, exist_ok=True)
    filepath = os.path.join(DATA_DIR, filename)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def get_users():
    """Get all users"""
    return load_json_file('users.json')

def save_users(users):
    """Save users to file"""
    save_json_file('users.json', users)

def get_db():
    """Get main database"""
    return load_json_file('db.json')

def save_db(db):
    """Save main database"""
    save_json_file('db.json', db)

def get_faqs():
    """Get FAQs"""
    return load_json_file('faqs.json')

def get_next_id(items):
    """Get next ID for a list of items"""
    if not items:
        return 1
    return max(item.get('id', 0) for item in items) + 1
