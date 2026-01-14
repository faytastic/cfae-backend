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
            import oracledb
            import os

            pw = os.environ.get("CFAEATP_ADMIN_PASSWORD")
            if not pw:
                return jsonify({"error": "DB password not configured"}), 500

            conn = oracledb.connect(
                user="ADMIN",
                password=pw,
                dsn="cfaeatp_low",
                config_dir="/home/opc/wallets/cfae-atp",
                tcp_connect_timeout=5,
                retry_count=0
            )

            cur = conn.cursor()
            cur.execute(
                """
                INSERT INTO cfae_contacts (name, email, message)
                VALUES (:1, :2, :3)
                """,
                [name, email, message]
            )
            conn.commit()

            cur.close()
            conn.close()

        except Exception as e:
            print("DB insert failed:", str(e))
            return jsonify({"error": "DB insert failed"}), 500

        return jsonify({"status": "ok", "message": "Saved to DB"}), 200

