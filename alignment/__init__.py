import os
from flask import Flask
from dotenv import load_dotenv

# Load ENV variables from .env file
load_dotenv()

def create_app():
    app = Flask(__name__)
    app.config.from_mapping(
        SECRET_KEY = 'test',
        DATABASE = os.path.join(app.instance_path, 'alignment.sql'),
    )

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    
    from . import db 
    db.init_app(app)

    from . import frontend
    app.register_blueprint(frontend.bp)

    # Test page
    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    return app
