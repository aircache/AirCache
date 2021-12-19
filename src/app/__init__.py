import os
from flask import Flask

config = {
    "DEBUG": os.getenv('DEBUG', 'development'),
    "HOST": os.getenv('HOST'),
    "PORT": int(os.getenv('PORT', '5001'))
}

def create_app():
    """Construct the core application."""
    app = Flask(__name__)
    app.config.from_mapping(config)
    with app.app_context():
        from . import routes  # Import routes
        return app