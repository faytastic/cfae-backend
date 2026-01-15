from flask import Flask

def create_app():
    app = Flask(__name__, template_folder="../templates")


    # Import routes after app is created
    from .routes import register_routes
    register_routes(app)

    # Register admin routes
    from .admin_routes import admin_bp
    app.register_blueprint(admin_bp)

    return app

