"""Page rendering routes."""

from flask import Blueprint, render_template
from ..services.quiz_service import QuizService
from ..utils.helpers import format_quiz

page_bp = Blueprint('pages', __name__)


@page_bp.route('/')
def index():
    """Render home page."""
    return render_template('home.html')


@page_bp.route('/quizzes')
def quizzes():
    """Render quizzes management page."""
    return render_template('quizzes.html')


@page_bp.route('/quiz/<int:quiz_id>')
def quiz_detail(quiz_id):
    """Render single quiz detail page."""
    quiz = QuizService.get_quiz(quiz_id)
    if not quiz:
        return render_template('404.html'), 404
    formatted = format_quiz(quiz)
    return render_template('quiz_detail.html', quiz=formatted)
