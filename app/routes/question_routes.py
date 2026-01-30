"""Question answering routes."""

from flask import Blueprint, jsonify, request
from ..services.quiz_service import QuizService

question_bp = Blueprint('question', __name__, url_prefix='/api/answer')


@question_bp.route('/<int:quiz_id>', methods=['POST'])
def answer_question(quiz_id):
    """Submit an answer to a quiz question."""
    payload = request.get_json(silent=True) or {}
    user_answer = payload.get("answer", "").strip()
    
    if not user_answer:
        return jsonify({"error": "Answer is required."}), 400
    
    quiz = QuizService.get_quiz(quiz_id)
    if not quiz:
        return jsonify({"error": "Quiz not found."}), 404
    
    is_correct = user_answer.lower() == quiz["answer"].lower()
    
    return jsonify({
        "quiz_id": quiz_id,
        "question": quiz["question"],
        "user_answer": user_answer,
        "correct_answer": quiz["answer"],
        "is_correct": is_correct
    })
