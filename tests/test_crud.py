"""Test fixtures and utilities for CRUD testing."""

import pytest
from app import create_app
from app.utils.seeder import load_seed_data


@pytest.fixture
def client():
    """Create a test client for the Flask app."""
    app = create_app()
    app.config['TESTING'] = True
    with app.test_client() as test_client:
        yield test_client


@pytest.fixture
def seed_data():
    """Load seed data for tests."""
    return load_seed_data()


class TestQuizCRUD:
    """Test CRUD operations for quizzes."""

    def test_list_quizzes(self, client, seed_data):
        """Test GET /api/quizzes returns list of quizzes."""
        response = client.get('/api/quizzes')
        assert response.status_code == 200
        data = response.get_json()
        assert isinstance(data, list)
        # Should have at least one quiz (from seed or demo)
        assert len(data) >= 1

    def test_quiz_structure(self, client, seed_data):
        """Test seed data has required fields."""
        # Test structure of seed data, not the demo API response
        assert len(seed_data) >= 1
        quiz = seed_data[0]
        
        # Check required fields in seed data
        required_fields = ['quiz_id', 'word', 'question', 'choices', 'correct_answer']
        for field in required_fields:
            assert field in quiz, f"Missing field: {field}"

    def test_seed_data_structure(self, seed_data):
        """Test seed data JSON structure is valid."""
        assert isinstance(seed_data, list)
        assert len(seed_data) >= 1
        
        # Check each quiz in seed has required fields
        required_quiz_fields = [
            'quiz_id', 'word', 'part_of_speech', 'meaning_vi',
            'question', 'choices', 'correct_answer', 'explanation'
        ]
        
        for quiz in seed_data:
            for field in required_quiz_fields:
                assert field in quiz, f"Quiz missing field: {field}"
            
            # Validate choices structure
            assert isinstance(quiz['choices'], list)
            assert len(quiz['choices']) == 4
            for choice in quiz['choices']:
                assert 'key' in choice
                assert 'value' in choice
                assert choice['key'] in ['A', 'B', 'C', 'D']
            
            # Validate correct_answer is one of the choice keys
            assert quiz['correct_answer'] in ['A', 'B', 'C', 'D']

    def test_seed_data_uniqueness(self, seed_data):
        """Test seed data doesn't have duplicate quizzes."""
        quiz_ids = [q['quiz_id'] for q in seed_data]
        assert len(quiz_ids) == len(set(quiz_ids)), "Duplicate quiz_id found in seed data"
