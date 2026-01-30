"""Business logic related to quizzes."""

class QuizService:
    @staticmethod
    def get_demo_quizzes():
        """Return a static list of demo quizzes for examples and tests."""
        return [
            {"id": 1, "question": "What's 2+2?", "options": ["3", "4", "5"], "answer": "4"},
            {"id": 2, "question": "Capital of France?", "options": ["Paris", "London"], "answer": "Paris"},
        ]
