"""Tests for quiz service and app routes."""

import pytest
from app import create_app
from app.services.quiz_service import QuizService


@pytest.fixture
def client():
    """Create a test client for the Flask app."""
    app = create_app()
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


# Service tests
class TestQuizService:
    def test_get_demo_quizzes_returns_list(self):
        """Test get_demo_quizzes returns a list."""
        quizzes = QuizService.get_demo_quizzes()
        assert isinstance(quizzes, list)

    def test_get_demo_quizzes_has_items(self):
        """Test get_demo_quizzes returns at least one item."""
        quizzes = QuizService.get_demo_quizzes()
        assert len(quizzes) >= 1

    def test_get_demo_quizzes_has_required_fields(self):
        """Test quiz items have required fields."""
        quizzes = QuizService.get_demo_quizzes()
        for quiz in quizzes:
            assert 'id' in quiz
            assert 'question' in quiz
            assert 'options' in quiz
            assert 'answer' in quiz


# Route tests
class TestRoutes:
    def test_index_route_returns_200(self, client):
        """Test index route returns 200 OK."""
        response = client.get('/')
        assert response.status_code == 200

    def test_index_route_returns_html(self, client):
        """Test index route returns HTML content."""
        response = client.get('/')
        assert b'Quiz' in response.data

    def test_api_quizzes_returns_200(self, client):
        """Test API quizzes endpoint returns 200 OK."""
        response = client.get('/api/quizzes')
        assert response.status_code == 200

    def test_api_quizzes_returns_json(self, client):
        """Test API quizzes endpoint returns JSON."""
        response = client.get('/api/quizzes')
        assert response.content_type == 'application/json'

    def test_api_quizzes_json_structure(self, client):
        """Test API quizzes returns correct JSON structure."""
        response = client.get('/api/quizzes')
        data = response.get_json()
        assert isinstance(data, list)
        assert len(data) >= 1
        assert 'question' in data[0]
