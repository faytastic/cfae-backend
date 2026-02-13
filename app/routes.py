from app.db import get_connection
from flask import request, jsonify

def register_routes(app):
    @app.route("/")
    def home():
        return "CFAE backend is running."

    @app.route("/health", methods=["GET"])
    def health():
        return jsonify({"status": "ok"}), 200

    @app.route("/api/contact", methods=["POST"])
    def contact():
        data = request.json or {}

        name = data.get("name", "").strip()
        email = data.get("email", "").strip()
        message = data.get("message", "").strip()

        if not name or not email or not message:
            return jsonify({"error": "All fields are required"}), 400

        try:
            conn = get_connection()

            with conn.cursor() as cur:
                cur.execute(
                    """
                    INSERT INTO cfae_contacts (name, email, message)
                    VALUES (:1, :2, :3)
                    """,
                    [name, email, message]
                )

            conn.commit()
            conn.close()

        except Exception as e:
            print("DB insert failed:", str(e))
            return jsonify({"error": "DB insert failed"}), 500

        return jsonify({"status": "ok", "message": "Saved to DB"}), 200
