import os
from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from dotenv import load_dotenv

# Load ENV variables from .env file
load_dotenv()

def create_app():
    app = Flask(__name__)
    app.config.from_mapping(
        SECRET_KEY = 'test',
        DATABASE = os.path.join(app.instance_path, 'alignment.sql'),
    )

    # Initialize Flask-Bootstrap extension
    bootstrap = Bootstrap(app)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    
    from . import db 
    db.init_app(app)

    from . import frontend
    app.register(frontend.index)

    return app
