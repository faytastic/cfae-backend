class Config:
    DEBUG = False

class DevConfig(Config):
    DEBUG = True

class ProdConfig(Config):
    DEBUG = False
