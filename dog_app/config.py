"""
    Configuration file for the app
"""

WTF_CSRF_ENABLED = True
SECRET_KEY = 'you-will-never-guess'

# SQL alchemy configurations
SQLALCHEMY_DATABASE_URI = 'postgresql://microblog_user:microblog_password@localhost:5432/microblog'
SQLALCHEMY_TRACK_MODIFICATIONS = True


