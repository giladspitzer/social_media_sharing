from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from backend import Config as config

db = SQLAlchemy()
migrate = Migrate()


def create_app(config_class=config.Config):
    application = Flask(__name__)
    application.config.from_object(config_class)

    with application.app_context():
        db.init_app(application)
        migrate.init_app(application, db)
        from backend import models

    from backend.api.main import bp as main_bp
    application.register_blueprint(main_bp)

    return application


app = create_app()
app.app_context().push()
from backend import models