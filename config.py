# config.py

class Config(object):
  DEBUG = True
  TESTING = False
  SQLALCHEMY_ECHO = True



class DevelopmentConfig(Config):
  "Empty"

class ProductionConfig(Config):
  DEBUG = False
  SQLALCHEMY_ECHO = False

class TestingConfig(Config):
  TESTING = True

app_config = {
  'development': DevelopmentConfig,
  'production': ProductionConfig,
  'testing': TestingConfig
}