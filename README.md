# Quiz_En — Flask Project Template

Cấu trúc mẫu dự án Flask (route, service, util, view).

Hướng dẫn nhanh:

1. Tạo virtualenv (nếu cần):
   python -m venv myenv
2. Kích hoạt:
   source myenv/bin/activate
3. Cài dependencies:
   pip install -r requirements.txt
4. Chạy ứng dụng:
   python run.py

Kiến trúc (gợi ý):
- `app/routes` — chứa blueprints và các route (HTTP handlers)
- `app/services` — logic nghiệp vụ, xử lý dữ liệu
- `app/utils` — helper/utility functions
- `templates` — Jinja2 templates cho view

Thêm tests với `pytest` và mở rộng theo nhu cầu.
