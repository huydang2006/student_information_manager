# app/__init__.py
from flask import Flask, redirect, url_for
from app.config import config
import os
from app.database.init_db import init_database


def create_app(config_name=None):
    """Application factory function"""
    
    # Determine configuration
    if config_name is None:
        config_name = os.getenv('FLASK_ENV', 'development')
    
    cfg = config.get(config_name, config['default'])
    
    # Create Flask app
    app = Flask(__name__, template_folder='templates', static_folder='static')
    app.config.from_object(cfg)
        # --- Chạy init database ngay lập tức ---
    if os.getenv("INIT_DB", "true") == "true":
        with app.app_context():
            init_database()
    
    # Register blueprints
    from app.routes.home import home_bp
    from app.routes.students import students_bp
    from app.routes.instructors import instructors_bp
    from app.routes.programs import programs_bp
    from app.routes.tuitions import tuitions_bp
    
    app.register_blueprint(home_bp)
    app.register_blueprint(students_bp)
    app.register_blueprint(instructors_bp)
    app.register_blueprint(programs_bp)
    app.register_blueprint(tuitions_bp)
    
    # Home route
    @app.route('/')
    def home():
        return redirect(url_for('home.describe'))

    # Error handlers
    @app.errorhandler(404)
    def page_not_found(e):
        return {'error': 'Page not found'}, 404
    
    @app.errorhandler(500)
    def internal_error(e):
        return {'error': 'Internal server error'}, 500
    
    return app
