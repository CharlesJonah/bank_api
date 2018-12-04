"""Application configuration."""

from os import getenv


class BaseConfig(object):
    """Base configuration class."""

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = getenv('APP_SECRET_KEY')


class TestingConfig(BaseConfig):
    """Configuration for testing environment."""

    DEBUG = True
    SQLALCHEMY_DATABASE_URI = getenv('TESTING_DATABASE_URI')


class DevelopmentConfig(BaseConfig):
    """Configuration for development environment."""

    DEBUG = True
    SQLALCHEMY_DATABASE_URI = getenv('DEVELOPMENT_DATABASE_URL')


class ProductionConfig(BaseConfig):
    """Configuration for production environment."""

    DEBUG = True
    SQLALCHEMY_DATABASE_URI = getenv('DATABASE_URL')


configurations = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig
}
