from alignment import create_app

def test_config():
    """Make sure instances of the app that are not being tested have the correct configurations.
    """
    assert not create_app().testing
    assert create_app({'TESTING': True}).testing

