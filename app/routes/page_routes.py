"""Page rendering routes."""

from flask import Blueprint, render_template
from ..services.quiz_service import QuizService
from ..utils.helpers import format_quiz

page_bp = Blueprint('pages', __name__)


def _get_page_context(page_type, **kwargs):
    """Get page context with headers and metadata."""
    contexts = {
        'home': {
            'page_title': '🎓 Welcome to Quiz App',
            'page_subtitle': 'Create, Practice, and Master Your Knowledge',
            'current_route': 'home',
            'show_breadcrumb': False,
        },
        'quizzes_list': {
            'page_title': '📚 Browse Quizzes',
            'page_subtitle': 'Choose a quiz to test your knowledge',
            'current_route': 'quizzes_list',
            'show_breadcrumb': True,
            'breadcrumbs': [
                {'label': 'Home', 'url': '/'},
                {'label': 'Browse Quizzes', 'url': '/quizzes-list'},
            ],
        },
        'quizzes_manage': {
            'page_title': '📝 Quiz Management',
            'page_subtitle': 'Create, edit, and manage your quiz questions',
            'current_route': 'quizzes_manage',
            'show_breadcrumb': True,
            'breadcrumbs': [
                {'label': 'Home', 'url': '/'},
                {'label': 'Manage Quizzes', 'url': '/quizzes'},
            ],
        },
        'quiz_attempt': {
            'page_title': '🎯 Take Quiz',
            'page_subtitle': 'Answer each question carefully',
            'current_route': 'quiz_attempt',
            'show_breadcrumb': True,
            'breadcrumbs': [
                {'label': 'Home', 'url': '/'},
                {'label': 'Browse', 'url': '/quizzes-list'},
                {'label': 'Quiz', 'url': '#'},
            ],
        },
        'generator': {
            'page_title': '🤖 AI Quiz Generator',
            'page_subtitle': 'Generate quiz questions from vocabulary using AI',
            'current_route': 'generator',
            'show_breadcrumb': True,
            'breadcrumbs': [
                {'label': 'Home', 'url': '/'},
                {'label': 'Generator', 'url': '/generator'},
            ],
        },
    }
    context = contexts.get(page_type, {})
    context.update(kwargs)
    return context


@page_bp.route('/')
def index():
    """Render home page."""
    context = _get_page_context('home')
    return render_template('home.html', **context)


@page_bp.route('/quizzes')
def quizzes():
    """Render quizzes management page."""
    context = _get_page_context('quizzes_manage')
    return render_template('quizzes.html', **context)


@page_bp.route('/quizzes-list')
def quizzes_list():
    """Render quizzes browse page."""
    context = _get_page_context('quizzes_list')
    return render_template('list_quizzes.html', **context)


@page_bp.route('/quiz/<int:quiz_id>')
def quiz_detail(quiz_id):
    """Render single quiz attempt page."""
    quiz = QuizService.get_quiz(quiz_id)
    if not quiz:
        return render_template('404.html'), 404
    formatted = format_quiz(quiz)
    context = _get_page_context(
        'quiz_attempt',
        quiz=formatted,
        breadcrumbs=[
            {'label': 'Home', 'url': '/'},
            {'label': 'Browse', 'url': '/quizzes-list'},
            {'label': 'Quiz', 'url': f'/quiz/{quiz_id}'},
        ]
    )
    return render_template('quiz_attempt.html', **context)


@page_bp.route('/generator')
def generator():
    """Render quiz generator page."""
    context = _get_page_context('generator')
    return render_template('generator.html', **context)
