# routes package

from .main import main_bp
from .quiz_routes import quiz_bp
from .question_routes import question_bp
from .page_routes import page_bp
from .generator_routes import generator_bp
from .template_routes import template_bp

__all__ = ['main_bp', 'quiz_bp', 'question_bp', 'page_bp', 'generator_bp', 'template_bp']