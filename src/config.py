"""Flask configuration variables."""
import os
from os import environ, path

basedir = path.abspath(path.dirname(__file__))


class Config:
    """Set Flask configuration from .env file."""

    # Database
    SQLALCHEMY_DATABASE_URI = "mysql://root:password@localhost/se_project"
    # Use the below URI when using xampp 
    # SQLALCHEMY_DATABASE_URI = "mysql://seteam18:evlxey@localhost/BeerGame?unix_socket=/opt/lampp/var/mysql/mysql.sock"
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class BaseConfig(object):
    DEBUG = False
    # shortened for readability

class TestConfig(BaseConfig):
    DEBUG = True
    TESTING = True
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'


class DevelopmentConfig(BaseConfig):
    DEBUG = True


class ProductionConfig(BaseConfig):
    DEBUG = False