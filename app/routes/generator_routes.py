"""Routes để generate quiz từ vocabulary."""

from flask import Blueprint, jsonify, request
from ..services.ai_quiz_generator import AIQuizGenerator

generator_bp = Blueprint('generator', __name__, url_prefix='/api/generator')


@generator_bp.route('/generate', methods=['POST'])
def generate_quizzes():
    """
    Generate quiz từ vocabulary.
    
    Request body:
    {
        "vocabulary": "word1, word2, word3" or ["word1", "word2", "word3"],
        "num_questions": 5  (optional, default: 5)
    }
    
    Response:
    {
        "success": true,
        "quizzes": [...],
        "message": "Generated and saved 5 quizzes"
    }
    """
    payload = request.get_json(silent=True) or {}
    vocabulary = payload.get("vocabulary", "").strip()
    num_questions = payload.get("num_questions", 5)
    
    if not vocabulary:
        return jsonify({
            "success": False,
            "message": "Vocabulary is required"
        }), 400
    
    if not isinstance(num_questions, int) or num_questions < 1 or num_questions > 20:
        return jsonify({
            "success": False,
            "message": "num_questions must be between 1 and 20"
        }), 400
    
    result = AIQuizGenerator.generate_and_save_quizzes(vocabulary, num_questions)
    
    status_code = 201 if result["success"] else 400
    return jsonify(result), status_code


@generator_bp.route('/preview', methods=['POST'])
def preview_quizzes():
    """
    Preview quiz từ vocabulary (không save).
    
    Request body:
    {
        "vocabulary": "word1, word2, word3" or ["word1", "word2", "word3"],
        "num_questions": 5  (optional, default: 5)
    }
    
    Response:
    {
        "success": true,
        "quizzes": [...]
    }
    """
    payload = request.get_json(silent=True) or {}
    vocabulary = payload.get("vocabulary", "").strip()
    num_questions = payload.get("num_questions", 5)
    
    if not vocabulary:
        return jsonify({
            "success": False,
            "quizzes": [],
            "message": "Vocabulary is required"
        }), 400
    
    if not isinstance(num_questions, int) or num_questions < 1 or num_questions > 20:
        return jsonify({
            "success": False,
            "quizzes": [],
            "message": "num_questions must be between 1 and 20"
        }), 400
    
    quizzes = AIQuizGenerator.generate_quiz_from_vocabulary(vocabulary, num_questions)
    
    return jsonify({
        "success": len(quizzes) > 0,
        "quizzes": quizzes
    })
