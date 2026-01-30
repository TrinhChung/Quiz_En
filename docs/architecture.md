# Kiến trúc tổng quan (Quiz System)

## Mục tiêu
Xây dựng hệ thống Quiz theo cấu trúc JSON đã chốt:
- 1 quiz = 1 câu điền chỗ trống (fill-in-the-blank)
- 4 đáp án (A–D)
- Có nghĩa tiếng Việt + giải thích ngắn gọn vì sao chọn đáp án
- Từ nhiều nghĩa → nhiều quiz (tách theo nghĩa)
- Quiz sinh từ Gemini API, lưu SQLite, phục vụ HTML đọc và làm quiz

## Data Model (JSON Quiz)
Một quiz có cấu trúc chuẩn:

```json
{
  "quiz_id": "string",
  "word": "string",
  "part_of_speech": "preposition | conjunction | quantifier | phrasal_verb | adverb | expression",
  "meaning_vi": "string",
  "question": {
    "sentence": "string",
    "blank_position": "____"
  },
  "choices": [
    { "key": "A", "value": "string" },
    { "key": "B", "value": "string" },
    { "key": "C", "value": "string" },
    { "key": "D", "value": "string" }
  ],
  "correct_answer": "A | B | C | D",
  "explanation": {
    "vi": "string"
  }
}
```

## Cấu trúc thư mục chính

```text
app/
├─ routes/                 # Blueprint & HTTP handlers
│  ├─ main_routes.py       # HTML pages
│  └─ api_quiz_routes.py   # JSON API for quizzes
├─ services/
│  ├─ quiz_service.py      # Orchestrate generate + validate + query
│  └─ gemini_service.py    # Call Gemini, parse JSON
├─ repositories/           # DB access layer (khuyến nghị)
│  ├─ vocab_repo.py
│  └─ quiz_repo.py
├─ models/                 # SQLAlchemy models (SQLite)
│  ├─ vocabulary.py
│  ├─ quiz.py
│  └─ quiz_choice.py
├─ utils/
│  ├─ schema_validate.py   # JSON schema validation
│  └─ text_normalize.py    # normalize/dedupe/sanitize
├─ templates/              # Jinja2 templates
└─ __init__.py             # create_app()
run.py                     # Entrypoint
tests/                     # pytest
docs/                      # Markdown docs
```

## Luồng xử lý (Simplified)

```text
(1) Input words list / vocabulary_ids
     ↓
(2) Gemini Service: generate quiz JSON (strict)
     ↓
(3) Validate JSON (schema + business rules)
     ↓
(4) Save to SQLite (quiz + choices)
     ↓
(5) Client GET quizzes -> render HTML/JS quiz
```

## Quyết định thiết kế
- App factory (`create_app`) để test dễ, cấu hình theo env
- Routes chỉ làm HTTP mapping; logic nằm trong services
- Gemini bắt buộc trả JSON strict; luôn validate trước khi insert DB
- DB lưu dạng normalized (quiz, quiz_choice) nhưng API trả JSON đúng structure

## Điểm mở rộng
- Thêm `quiz_attempts` để tracking đúng/sai (spaced repetition)
- Thêm `tags`/`level` để phân loại quiz
- Thêm export: JSON dump / CSV / Anki
