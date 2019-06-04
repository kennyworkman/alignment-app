import os
from flask import Flask

def create_app():
    # Initialize instance of Flask app and configure
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite')
    )

    # Make sure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    
    # Register various views with the main app instance
    from flaskr.model import db
    db.init_app(app)
    
    from flaskr.frontend import frontend
    app.register_blueprint(frontend)

    # Test page
    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    return app
