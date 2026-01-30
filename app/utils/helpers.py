"""Utility helpers used across the app."""

def format_quiz(quiz: dict) -> dict:
    """Return a minimal representation of a quiz for views."""
    return {
        "id": quiz.get("id"),
        "question": quiz.get("question"),
    }
