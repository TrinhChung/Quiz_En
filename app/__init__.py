"""Flask application factory and package init."""

from flask import Flask


def create_app(config_object=None):
    """Create and configure the Flask app."""
    app = Flask(__name__, template_folder='templates', static_folder='static')

    if config_object:
        app.config.from_object(config_object)

    # Register blueprints
    from .routes.main import main_bp
    app.register_blueprint(main_bp)

    return app
