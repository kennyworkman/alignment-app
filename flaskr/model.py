import sqlite3
from flask import g, current_app

# Save database connection in Request Context
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(# Fill in later) 
    return db

# Add to 'teardown_appcontext' handler; Makes sure database connection is closed when Request ends
@app.teardown_appcontext
def teardown_db():
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

# Initialize database based on schema
def init_db():
    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))
    
