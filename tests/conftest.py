import os
from tempfile import NamedTemporaryFile

import pytest

from alignment import create_app
from alignment.db import init_db

@pytest.fixture
def app():
    f = NamedTemporaryFile(delete=False, dir='/tmp')

    app = create_app({
        'TESTING': True,
        'DATABASE': f.name,
    })

    with app.app_context():
        init_db()

    yield app 

    f.close
    os.unlink(f.name)

# Client fixture can make requests without running the server
@pytest.fixture
def client(app):
    return app.test_client()

# Runner can call Click commands to simulate command line commands.
@pytest.fixture
def runner(app):
    return app.test_cli_runner()
