from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
""" Database instance.

db is a default database instance of Flask-SQLAlchemy.
It uses SQLite3 as the backing database.
It is configured (in app.py) to save to the data.db file within app directory.
"""
