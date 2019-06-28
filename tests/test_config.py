from alignment import create_app

def test_config():
    """Ensure different configurations of app instances have proper attributes
    """
    assert not create_app().testing
    assert create_app({'TESTING': True}).testing
