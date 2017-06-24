#! /C/Users/zfeng/AppData/Local/Continuum/Anaconda3/envs/aind-dog/python

"""
    A simple dog recogniser app for fun
"""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import views
import models


app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)


"""
    Logging error message to a file
"""
if not app.debug:
    import logging
    from logging.handlers import RotatingFileHandler
    file_handler = RotatingFileHandler('tmp/server.log', 'a', 1 * 1024 * 1024, 10)
    file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('dog_app startup')

if __name__ == "__main__":
    app.run(debug=True)
