# Routes & API (Quiz JSON Spec)

## Mục tiêu
API trả dữ liệu theo đúng cấu trúc quiz JSON đã chốt.
HTML pages là thin layer để load quiz và hiển thị.

## HTML Endpoints
- `GET /` — Trang index
- `GET /quiz` — Trang làm quiz (render)

## API Endpoints (v1)

### 1) List quizzes
- `GET /api/quizzes`

Query params gợi ý:
- `limit=20`
- `offset=0`
- `pos=preposition|quantifier|conjunction|phrasal_verb|adverb|expression`
- `level=easy|medium|hard`
- `random=1`

Response: mảng quiz objects (theo JSON structure)

### 2) Get quiz by id
- `GET /api/quizzes/<id>`

Response: 1 quiz object

### 3) Generate quizzes from vocabulary ids
- `POST /api/quizzes/generate`

Body:
```json
{ "vocabulary_ids": [1,2,3], "per_word": 1 }
```

Flow:
- Load word(s) từ DB
- Call Gemini
- Validate JSON
- Save quiz & choices
- Return created quiz ids

### 4) Import vocabulary list
- `POST /api/vocabulary/import`

Body:
```json
{ "words": ["in", "by", "a few"] }
```

Flow:
- Normalize/dedupe
- Save vào bảng vocabulary
- Return ids

### 5) Health
- `GET /health`

## Quy tắc dữ liệu (Validation Rules)
Trước khi lưu DB:
- `choices` phải đúng 4 phần tử, keys A–D
- `correct_answer` phải nằm trong A–D
- `question.sentence` phải chứa `"____"` (khuyến nghị đúng 1 lần)
- `word` không được rỗng
- `meaning_vi` và `explanation.vi` bắt buộc có

Nếu fail:
- trả `422 Unprocessable Entity` với message ngắn gọn
