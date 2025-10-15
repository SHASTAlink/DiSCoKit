"""
WSGI entry point for production deployment with Gunicorn or uWSGI.
"""

from app import create_app

app = create_app()

if __name__ == "__main__":
    app.run()