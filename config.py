import os

class BaseConfig:
    DEBUG = False
    SECRET_KEY = os.getenv("SECRET_KEY")

class DevelopmentConfig(BaseConfig):
    DEBUG = True
    SECRET_KEY = os.getenv("SECRET_KEY", "development-key")

class ProductionConfig(BaseConfig):
    DEBUG = False
    SECRET_KEY = os.getenv("SECRET_KEY")
