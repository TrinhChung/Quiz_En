"""Template cho AI Quiz Generator."""

import os
from flask import Blueprint, render_template

template_bp = Blueprint('templates', __name__)


@template_bp.route('/generator')
def generator_page():
    """Render trang tạo quiz từ vocabulary."""
    has_api_key = bool(os.getenv("GEMINI_API_KEY"))
    return render_template('generator.html', has_api_key=has_api_key)
