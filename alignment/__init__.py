"""
    alignment
    ~~~~~~~~~
    A Flask based web application for gene alignment. It attempts to follow
    best documentation and practice patterns.
"""

import os
from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from dotenv import load_dotenv

# Loads environment variables from .env file in project root dir.
load_dotenv()


def create_app(test_config=None):
    """Creates and configures an instance of the Flask application.

    To load a development or production configuration, leave out the optional
    dictionary parameter. Only use this to override the default configs for
    something like testing.

    :param test_config: An optional dictionary of configuration mappings
    :type test_config: dict or None
    :return: a Flask() instance
    """

    app = Flask(__name__, instance_relative_config=True)

    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'alignment.sql'),
    )

    # Overriding the app config only occurs if there is a config.py present.
    # Standard configuration from mapping occurs otherwise.
    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    Bootstrap(app)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # Registers 'init-db' command line command
    # Adds close_db() to app.teardown_appcontext(), no need of an
    # explicit call
    from . import db
    db.init_app(app)

    from . import frontend
    app.register_blueprint(frontend.bp)

    return app
