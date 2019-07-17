""""
    wsgi
    ~~~~
    Specififes an entry point for a WSGI-based server (Gunicorn recommended).
"""

from alignment import create_app

# Calling module from command line allows convenient debug/production mode
if __name__ == "__main__":
    app = create_app()
    app.run("0.0.0.0", debug=True)
