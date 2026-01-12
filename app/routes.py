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

        print("New contact submission:")
        print(f"Name: {name}")
        print(f"Email: {email}")
        print(f"Message: {message}")

        return jsonify({"status": "ok", "message": "Form received"})
