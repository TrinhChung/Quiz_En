"""Entrypoint to run the Flask app locally."""

from app import create_app

app = create_app()

if __name__ == "__main__":
    # Development server
    app.run(debug=True, host="0.0.0.0", port=1132)
