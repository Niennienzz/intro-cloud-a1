from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
""" Database instance.

Variable db is a default database instance of Flask-SQLAlchemy.
It uses SQLite3 as the backing database, and configured (in app.py)
to save to the data.db file within app directory.
"""
