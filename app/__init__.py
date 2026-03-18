from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_restful import Api
from config import Config

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message = 'Пожалуйста, войдите для доступа.'

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    # Регистрация blueprint'ов
    from app.routes.auth import auth_bp
    from app.routes.main import main_bp
    from app.routes.profile import profile_bp
    from app.routes.admin import admin_bp

    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(main_bp)
    app.register_blueprint(profile_bp, url_prefix='/profile')
    app.register_blueprint(admin_bp, url_prefix='/admin')

    # REST API (если нужно, иначе можно закомментировать)
    api = Api(app)
    from app.api.resources import UserResource, AppointmentResource, ServiceResource, MasterResource
    api.add_resource(UserResource, '/api/users', '/api/users/<int:id>')
    api.add_resource(AppointmentResource, '/api/appointments', '/api/appointments/<int:id>')
    api.add_resource(ServiceResource, '/api/services', '/api/services/<int:id>')
    api.add_resource(MasterResource, '/api/masters', '/api/masters/<int:id>')

    # CLI команды (именно они добавляют init-roles и create-admin)
    from app import cli
    cli.init_app(app)

    return app