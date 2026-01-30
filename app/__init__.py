"""Flask application factory and package init."""

from flask import Flask


def create_app(config_object=None):
    """Create and configure the Flask app."""
    app = Flask(__name__, template_folder='templates', static_folder='static')

    if config_object:
        app.config.from_object(config_object)

    # Register blueprints
    from .routes import main_bp, page_bp, quiz_bp, question_bp, generator_bp, template_bp
    app.register_blueprint(main_bp)
    app.register_blueprint(page_bp)
    app.register_blueprint(quiz_bp)
    app.register_blueprint(question_bp)
    app.register_blueprint(generator_bp)
    app.register_blueprint(template_bp)

    return app
