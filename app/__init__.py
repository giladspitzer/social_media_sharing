from flask import Flask


def create_app(config_class):
    application = Flask(__name__)
    application.config.from_object(config_class)

    from app.main import bp as main_bp
    application.register_blueprint(main_bp)

    return application

import models
