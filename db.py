from flask_sqlalchemy import SQLAlchemy

""" Database instance.

Variable db is a default database instance of Flask-SQLAlchemy.
It is configured to use MySQL as the backing database, and the database name is 'sys'.
All UserUI workers use a centralized MySQL server.
"""
db = SQLAlchemy()
