"""Database seeding utilities for loading test/demo data."""

import json
import os
from pathlib import Path


def load_seed_data(seed_file: str = "quiz_seed.json") -> list[dict]:
    """Load seed data from JSON file in seeds/ directory."""
    # Look for seed file relative to project root
    seed_path = Path(__file__).parent.parent.parent / "seeds" / seed_file
    
    if not seed_path.exists():
        raise FileNotFoundError(f"Seed file not found: {seed_path}")
    
    with open(seed_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def seed_database(app) -> int:
    """
    Load seed data and populate the database.
    Returns the number of records inserted.
    
    Example:
        from app import create_app
        from app.utils.seeder import seed_database
        
        app = create_app()
        with app.app_context():
            count = seed_database(app)
            print(f"Seeded {count} quizzes")
    """
    try:
        data = load_seed_data()
        # Placeholder: in the future, insert into DB using model
        # For now, just return count for demo
        return len(data)
    except Exception as e:
        print(f"Error seeding database: {e}")
        return 0
