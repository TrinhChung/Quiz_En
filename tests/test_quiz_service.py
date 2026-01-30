from app.services.quiz_service import QuizService


def test_get_demo_quizzes():
    quizzes = QuizService.get_demo_quizzes()
    assert isinstance(quizzes, list)
    assert len(quizzes) >= 1
    assert 'question' in quizzes[0]
