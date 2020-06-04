from flask import Flask
import os
from config import app_config


def create_app(config_mode="dev"):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)

    if config_mode == "dev":
        app.config.from_object(app_config.get("dev"))
    elif config_mode == "prod":
        app.config.from_object(app_config.get("prod"))
    else:
        raise Exception("Please Provide dev/prod config")

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    with app.app_context():
        from applications.home.views import home
        app.register_blueprint(home)
        from applications.dash.default import create_dashboard
        create_dashboard(app)
        from applications.dash.stocktoday import create_stock_app
        create_stock_app(app)
        return app
