from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import Config

db = SQLAlchemy()
migrate = Migrate()


def create_app(config_class=Config.Config):
    application = Flask(__name__)
    application.config.from_object(config_class)

    with application.app_context():
        db.init_app(application)
        migrate.init_app(application, db)
    from api.main import bp as main_bp
    application.register_blueprint(main_bp)

    return application


app = create_app()
app.app_context().push()
import models
