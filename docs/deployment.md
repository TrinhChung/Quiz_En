# Deployment & Runbook (Quiz System)

## Chạy local (Development)

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python run.py
```

## Biến môi trường khuyến nghị
- `FLASK_ENV=development|production`
- `DATABASE_URL=sqlite:///app.db`
- `GEMINI_API_KEY=...`
- `GEMINI_MODEL=...`

## Production (Khuyến nghị)
Chạy bằng Gunicorn:

```bash
gunicorn --bind 0.0.0.0:8000 run:app --workers 3
```

Khuyến nghị:
- Config qua environment variables
- Đặt sau reverse proxy (nginx) để TLS + static files
- Nếu public: thêm rate limit

## Docker (Optional)

```bash
gunicorn --bind 0.0.0.0:8000 run:app
```

Khuyến nghị thêm:
- `/health` endpoint
- Docker healthcheck
- Mount volume để persist file SQLite (nếu cần)

## Monitoring & Logs
- Log dạng structured (JSON)
- Log tối thiểu:
  - request_id
  - route
  - status_code
  - gemini_call_status (success/fail)
  - validation_fail_reason (nếu có)

## Health Check

```text
GET /health
```

Trả:
- `200 OK` khi app + DB ok
- (Optional) check Gemini connectivity nếu muốn
