"""Service để generate quiz từ từ vựng sử dụng AI."""

import os
import json
import re
import google.generativeai as genai

# Cấu hình Gemini API
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)


class AIQuizGenerator:
    """Generate quiz từ từ vựng sử dụng Gemini API."""
    
    @staticmethod
    def generate_quiz_from_vocabulary(vocabulary: str, num_questions: int = 5) -> list:
        """
        Generate quiz questions từ danh sách từ vựng.
        
        Args:
            vocabulary: Danh sách từ vựng (có thể là string hoặc list)
            num_questions: Số câu hỏi cần generate (default: 5)
        
        Returns:
            List of quiz objects: [{"question": "...", "options": [...], "answer": "..."}]
        """
        if not GEMINI_API_KEY:
            return []
        
        # Chuẩn bị prompt cho AI
        if isinstance(vocabulary, list):
            vocab_text = ", ".join(vocabulary)
        else:
            vocab_text = vocabulary
        
        prompt = f"""
Create {num_questions} multiple choice quiz questions from these vocabulary words: {vocab_text}

Return ONLY a valid JSON array with this format (no extra text):
[
  {{
    "question": "What does [word] mean?",
    "options": ["Option A", "Option B", "Option C", "Option D"],
    "answer": "Correct Option"
  }}
]

Requirements:
- Each question must have 4 options
- The "answer" field must be one of the options
- Make questions progressively harder
- Use different question types (definition, usage, synonym, antonym)
"""
        
        try:
            model = genai.GenerativeModel("gemini-pro")
            response = model.generate_content(prompt)
            
            # Lấy JSON từ response
            response_text = response.text
            
            # Tìm JSON array trong response
            json_match = re.search(r'\[[\s\S]*\]', response_text)
            if not json_match:
                return []
            
            json_str = json_match.group(0)
            quizzes = json.loads(json_str)
            
            return quizzes
        
        except Exception as e:
            print(f"Error generating quiz: {e}")
            return []
    
    @staticmethod
    def generate_and_save_quizzes(vocabulary: str, num_questions: int = 5) -> dict:
        """
        Generate quizzes từ vocabulary và save vào service.
        
        Returns:
            {"success": bool, "quizzes": list, "message": str}
        """
        quizzes = AIQuizGenerator.generate_quiz_from_vocabulary(vocabulary, num_questions)
        
        if not quizzes:
            return {
                "success": False,
                "quizzes": [],
                "message": "Failed to generate quizzes from AI"
            }
        
        # Import ở đây để tránh circular import
        from .quiz_service import QuizService
        
        saved_quizzes = []
        for quiz_data in quizzes:
            try:
                quiz = QuizService.create_quiz({
                    "question": quiz_data.get("question"),
                    "options": quiz_data.get("options", []),
                    "answer": quiz_data.get("answer")
                })
                saved_quizzes.append(quiz)
            except Exception as e:
                print(f"Error saving quiz: {e}")
        
        return {
            "success": len(saved_quizzes) > 0,
            "quizzes": saved_quizzes,
            "message": f"Generated and saved {len(saved_quizzes)} quizzes"
        }
