# Services — Thiết kế lớp nghiệp vụ (Quiz Generation)

## Trách nhiệm
Service layer xử lý toàn bộ nghiệp vụ:
- generate quiz từ Gemini
- validate/normalize JSON quiz
- lưu và truy vấn quiz từ SQLite
- không phụ thuộc Flask request/response

## Service chính

### 1) GeminiService
Trách nhiệm:
- Gọi Gemini API
- Bắt buộc trả JSON strict theo schema
- Parse JSON (fail-fast nếu có text thừa)
- Trả về object quiz (raw)

Gợi ý method:
- `generate_quizzes(words: list[str], per_word: int, pos_hint: str | None) -> list[dict]`

### 2) QuizService
Trách nhiệm:
- Orchestrate generate + validate + save
- Randomize choices (nếu cần) và cập nhật `correct_answer`
- Dedupe quiz theo `(word, meaning_vi, sentence)` để tránh trùng

Gợi ý method:
- `create_quizzes(vocabulary_ids: list[int], per_word: int) -> list[int]`
- `get_quizzes(limit: int, offset: int, random: bool, filters: dict) -> list[dict]`
- `get_quiz(quiz_id: int) -> dict`

## Validation & Normalization
Bắt buộc trước khi insert DB:
- Validate schema (jsonschema)
- Check business rules:
  - 4 choices
  - correct answer mapping đúng A–D
  - sentence có blank `"____"`
- Normalize:
  - trim spaces
  - unify punctuation
  - sanitize output để hiển thị HTML an toàn

## Error handling
- Gemini timeout/network → raise `ExternalServiceError` (map 502)
- JSON sai schema/rule → raise `QuizValidationError` (map 422)
- DB lỗi → raise `RepositoryError` (map 500)

## Testing
- Unit test `QuizService` bằng cách mock:
  - GeminiService trả JSON mẫu
  - QuizRepo thao tác DB giả
- Test validation rules:
  - thiếu field
  - choices != 4
  - correct_answer ngoài A–D
  - sentence không có blank
