"""Quiz CRUD routes."""

from flask import Blueprint, jsonify, request
from ..services.quiz_service import QuizService
from ..utils.helpers import format_quiz

quiz_bp = Blueprint('quiz', __name__, url_prefix='/api/quizzes')


def _validate_quiz_payload(payload, partial: bool = False):
    """Validate quiz payload."""
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


@quiz_bp.route('', methods=['GET'])
def list_quizzes():
    """Get all quizzes."""
    quizzes = QuizService.list_quizzes()
    return jsonify(quizzes)


@quiz_bp.route('', methods=['POST'])
def create_quiz():
    """Create a new quiz."""
    payload = request.get_json(silent=True) or {}
    errors = _validate_quiz_payload(payload)
    if errors:
        return jsonify({"errors": errors}), 400
    quiz = QuizService.create_quiz(payload)
    return jsonify(quiz), 201


@quiz_bp.route('/<int:quiz_id>', methods=['GET'])
def get_quiz(quiz_id):
    """Get a single quiz by ID."""
    quiz = QuizService.get_quiz(quiz_id)
    if not quiz:
        return jsonify({"error": "Quiz not found."}), 404
    return jsonify(quiz)


@quiz_bp.route('/<int:quiz_id>', methods=['PUT', 'PATCH'])
def update_quiz(quiz_id):
    """Update a quiz by ID."""
    payload = request.get_json(silent=True) or {}
    errors = _validate_quiz_payload(payload, partial=True)
    if errors:
        return jsonify({"errors": errors}), 400
    quiz = QuizService.update_quiz(quiz_id, payload)
    if not quiz:
        return jsonify({"error": "Quiz not found."}), 404
    return jsonify(quiz)


@quiz_bp.route('/<int:quiz_id>', methods=['DELETE'])
def delete_quiz(quiz_id):
    """Delete a quiz by ID."""
    deleted = QuizService.delete_quiz(quiz_id)
    if not deleted:
        return jsonify({"error": "Quiz not found."}), 404
    return jsonify({"status": "deleted"})
