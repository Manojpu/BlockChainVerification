import os

class Config:
    DEBUG = os.getenv('DEBUG', 'False') == 'True'
    SECRET_KEY = os.getenv('SECRET_KEY', 'your_secret_key')
    MONGODB_URI = os.getenv('MONGODB_URI', 'mongodb://localhost:27017/resume_verification')
    BLOCKCHAIN_URL = os.getenv('BLOCKCHAIN_URL', 'http://localhost:8545')
    JWT_SECRET = os.getenv('JWT_SECRET', 'your_jwt_secret')
    JWT_EXPIRATION = os.getenv('JWT_EXPIRATION', '1h')