from flask import Flask

def create_app():
    app = Flask(__name__)

    # Import routes after app is created
    from .routes import register_routes
    register_routes(app)

    return app
