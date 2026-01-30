# Quiz_En — Flask Project Template

Cấu trúc mẫu dự án Flask (route, service, util, view) theo hướng module hoá.

Hướng dẫn nhanh:

1. Tạo virtualenv (nếu cần):
   python -m venv myenv
2. Kích hoạt:
   source myenv/bin/activate
3. Cài dependencies:
   pip install -r requirements.txt
4. Chạy ứng dụng:
   python run.py

## Chạy bằng Docker

### Build & run nhanh (Dockerfile)
```bash
docker build -t quiz-en .
docker run --rm -p 5000:5000 quiz-en
```

### Chạy bằng docker-compose
```bash
docker compose up --build
```

Ứng dụng sẽ chạy tại: http://localhost:5000

Kiến trúc (gợi ý):
- `app/__init__.py` — app factory, đăng ký blueprint
- `app/routes` — chứa blueprints và các route (HTTP handlers)
- `app/services` — logic nghiệp vụ, xử lý dữ liệu
- `app/utils` — helper/utility functions
- `app/templates` — Jinja2 templates cho view
- `app/static` — tài nguyên tĩnh (CSS/JS/ảnh) nếu cần
- `tests` — kiểm thử với `pytest`

Gợi ý mở rộng:
- Tách cấu hình (dev/prod) vào module riêng.
- Thêm logging và error handlers.
