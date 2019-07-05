import os
from tempfile import mkstemp 

import pytest

from alignment import create_app
from alignment.db import init_db

@pytest.fixture
def app():
    # Temp file will house SQlite file for duration of the tests.
    f_handle, f_path = mkstemp()

    app = create_app({
        'TESTING': True,
        'DATABASE': f_path,
        'WTF_CSRF_ENABLED': False,
    })

    with app.app_context():
        init_db()

    yield app 

    os.close(f_handle)
    os.unlink(f_path)

# Client fixture can make requests without running the server
@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def new_client(app):
    return app.test_client()

# Runner can call Click commands to simulate command line commands.
@pytest.fixture
def runner(app):
    return app.test_cli_runner()
