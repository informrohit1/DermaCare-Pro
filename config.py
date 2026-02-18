import os

class Config:
    """Base configuration class."""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your_secret_key_here'  # You can change this to a random key for production
    UPLOAD_FOLDER = 'static/uploads'
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # Max file size: 16 MB
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # Disable track modifications to save resources
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'mysql://username:password@localhost/DermaCare'  # Replace with your actual DB credentials

    # Add more configuration variables as needed
