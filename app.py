from flask import Flask

def create_app():
    app = Flask(__name__)

    @app.route("/api/contact", methods=["GET"])
    def health_check():
        return {"status": "ok"}, 200

    return app


app = create_app()




