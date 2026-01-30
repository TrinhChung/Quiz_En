from flask import Blueprint, render_template, jsonify
from ..services.quiz_service import QuizService
from ..utils.helpers import format_quiz

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    quizzes = QuizService.get_demo_quizzes()
    formatted = [format_quiz(q) for q in quizzes]
    return render_template('index.html', quizzes=formatted)


@main_bp.route('/api/quizzes')
def api_quizzes():
    return jsonify(QuizService.get_demo_quizzes())
