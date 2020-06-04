import os

basedir = os.path.abspath(os.path.dirname("__file__"))
instance_dir = os.path.join(basedir, "instance")
app_dir = os.path.join(basedir, "applications")
dash_dir = os.path.join(app_dir, "dash")
dash_assets = os.path.join(dash_dir, "assets")


class BaseConfig(object):
    """Base config class"""
    SECRET_KEY = "46f65996-a956-45bf-b2e8-68c8eba2c2cc"
    DEBUG = True
    TESTING = False
    NEW_CONFIG_VARIABLE = "my value"


class ProductionConfig(BaseConfig):
    """Production specific config"""
    DEBUG = False
    SECRET_KEY = "46f65996-a956-45bf-b2e8-68c8eba2c2cc"


class DevelopmentConfig(BaseConfig):
    """Development environment specific config"""
    DEBUG = True
    TESTING = True
    SECRET_KEY = "46f65996-a956-45bf-b2e8-68c8eba2c2cc"


app_config = {
    "dev": DevelopmentConfig,
    "prod": ProductionConfig
}
