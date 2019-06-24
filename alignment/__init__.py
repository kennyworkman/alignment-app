import os
from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from dotenv import load_dotenv

# Load ENV variables from .env file
load_dotenv()

def create_app(test_config=None):
    app = Flask(__name__)
    
    app.config.from_mapping(
        SECRET_KEY = 'dev',
        DATABASE = os.path.join(app.instance_path, 'alignment.sql'),
    )
   
    if test_config is None:
        # Override default settings with production if a config file is in instance folder
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    # Initialize Flask-Bootstrap extension
    bootstrap = Bootstrap(app)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    
    from . import db 
    db.init_app(app)

    from . import frontend
    app.register_blueprint(frontend.bp)

    return app
