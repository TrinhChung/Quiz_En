"""Business logic related to quizzes."""


class QuizService:
    _quizzes = [
        {"id": 1, "question": "What's 2+2?", "options": ["3", "4", "5"], "answer": "4"},
        {"id": 2, "question": "Capital of France?", "options": ["Paris", "London"], "answer": "Paris"},
    ]
    _next_id = 3

    @classmethod
    def get_demo_quizzes(cls):
        """Return a static list of demo quizzes for examples and tests."""
        return [quiz.copy() for quiz in cls._quizzes]

    @classmethod
    def list_quizzes(cls):
        """Return all quizzes."""
        return cls.get_demo_quizzes()

    @classmethod
    def get_quiz(cls, quiz_id: int):
        """Return a single quiz by id."""
        return next((quiz for quiz in cls._quizzes if quiz["id"] == quiz_id), None)

    @classmethod
    def create_quiz(cls, payload: dict):
        """Create a new quiz and return it."""
        quiz = {
            "id": cls._next_id,
            "question": payload["question"].strip(),
            "options": payload["options"],
            "answer": payload["answer"].strip(),
        }
        cls._quizzes.append(quiz)
        cls._next_id += 1
        return quiz.copy()

    @classmethod
    def update_quiz(cls, quiz_id: int, payload: dict):
        """Update an existing quiz."""
        quiz = cls.get_quiz(quiz_id)
        if not quiz:
            return None
        if "question" in payload:
            quiz["question"] = payload["question"].strip()
        if "options" in payload:
            quiz["options"] = payload["options"]
        if "answer" in payload:
            quiz["answer"] = payload["answer"].strip()
        return quiz.copy()

    @classmethod
    def delete_quiz(cls, quiz_id: int) -> bool:
        """Delete a quiz by id."""
        for index, quiz in enumerate(cls._quizzes):
            if quiz["id"] == quiz_id:
                cls._quizzes.pop(index)
                return True
        return False
