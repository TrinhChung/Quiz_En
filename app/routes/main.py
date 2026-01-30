from flask import Blueprint, render_template, jsonify, request
from ..services.quiz_service import QuizService
from ..utils.helpers import format_quiz

main_bp = Blueprint('main', __name__)


def _validate_quiz_payload(payload, partial: bool = False):
    errors = {}
    if not payload:
        return {"payload": "Missing JSON body."}

    if not partial or "question" in payload:
        question = payload.get("question", "").strip()
        if not question:
            errors["question"] = "Question is required."

    if not partial or "options" in payload:
        options = payload.get("options")
        if not isinstance(options, list) or not options:
            errors["options"] = "Options must be a non-empty list."

    if not partial or "answer" in payload:
        answer = payload.get("answer", "").strip()
        if not answer:
            errors["answer"] = "Answer is required."

    return errors


@main_bp.route('/')
def index():
    quizzes = QuizService.list_quizzes()
    formatted = [format_quiz(q) for q in quizzes]
    return render_template('index.html', quizzes=formatted)


@main_bp.route('/api/quizzes', methods=['GET'])
def api_quizzes():
    return jsonify(QuizService.list_quizzes())


@main_bp.route('/api/quizzes', methods=['POST'])
def api_create_quiz():
    payload = request.get_json(silent=True) or {}
    errors = _validate_quiz_payload(payload)
    if errors:
        return jsonify({"errors": errors}), 400
    quiz = QuizService.create_quiz(payload)
    return jsonify(quiz), 201


@main_bp.route('/api/quizzes/<int:quiz_id>', methods=['GET'])
def api_get_quiz(quiz_id):
    quiz = QuizService.get_quiz(quiz_id)
    if not quiz:
        return jsonify({"error": "Quiz not found."}), 404
    return jsonify(quiz)


@main_bp.route('/api/quizzes/<int:quiz_id>', methods=['PUT', 'PATCH'])
def api_update_quiz(quiz_id):
    payload = request.get_json(silent=True) or {}
    errors = _validate_quiz_payload(payload, partial=True)
    if errors:
        return jsonify({"errors": errors}), 400
    quiz = QuizService.update_quiz(quiz_id, payload)
    if not quiz:
        return jsonify({"error": "Quiz not found."}), 404
    return jsonify(quiz)


@main_bp.route('/api/quizzes/<int:quiz_id>', methods=['DELETE'])
def api_delete_quiz(quiz_id):
    deleted = QuizService.delete_quiz(quiz_id)
    if not deleted:
        return jsonify({"error": "Quiz not found."}), 404
    return jsonify({"status": "deleted"})
