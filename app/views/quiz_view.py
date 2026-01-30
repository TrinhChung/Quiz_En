"""Quiz view models and rendering logic."""


class QuizViewModel:
    """View model for quiz display."""
    
    @staticmethod
    def format_for_list(quiz: dict) -> dict:
        """Format quiz for list display."""
        return {
            "id": quiz.get("id"),
            "question": quiz.get("question"),
            "option_count": len(quiz.get("options", [])),
        }
    
    @staticmethod
    def format_for_detail(quiz: dict) -> dict:
        """Format quiz for detail display."""
        return {
            "id": quiz.get("id"),
            "question": quiz.get("question"),
            "options": quiz.get("options", []),
            "answer": quiz.get("answer"),
        }
    
    @staticmethod
    def format_for_edit(quiz: dict) -> dict:
        """Format quiz for editing."""
        return {
            "id": quiz.get("id"),
            "question": quiz.get("question"),
            "options": quiz.get("options", []),
            "answer": quiz.get("answer"),
        }


class AnswerViewModel:
    """View model for answer feedback."""
    
    @staticmethod
    def format_answer_result(quiz_id: int, quiz: dict, user_answer: str, is_correct: bool) -> dict:
        """Format answer result for display."""
        return {
            "quiz_id": quiz_id,
            "question": quiz.get("question"),
            "user_answer": user_answer,
            "correct_answer": quiz.get("answer"),
            "is_correct": is_correct,
            "feedback": "Correct!" if is_correct else f"Wrong! The correct answer is: {quiz.get('answer')}",
        }
