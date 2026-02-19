import os
from flask import Flask
from dotenv import load_dotenv

import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration

from clerk_backend_api import Clerk
from supabase import create_client

# Import extensions from the extensions module
from .extensions import cors


def create_app(config_class=None):
    """
    Application factory function to create and configure the Flask app.
    """
    app = Flask(__name__)

    # Load environment variables early
    load_dotenv()

    # --- Configuration ---
    if config_class is None:
        # Determine configuration based on FLASK_ENV environment variable
        env = os.getenv("FLASK_ENV", "development")
        if env == "production":
            from .config import ProductionConfig
            config_class = ProductionConfig
        else:  # Default to development
            from .config import DevelopmentConfig
            config_class = DevelopmentConfig

    app.config.from_object(config_class)

    # --- Sentry Initialization ---
    sentry_dsn = app.config.get("SENTRY_DSN")
    if sentry_dsn:
        sentry_sdk.init(
            dsn=sentry_dsn,
            integrations=[
                FlaskIntegration(),
            ],
            traces_sample_rate=app.config.get("SENTRY_TRACES_SAMPLE_RATE", 1.0),
            profiles_sample_rate=app.config.get("SENTRY_PROFILES_SAMPLE_RATE", 1.0),
            environment=app.config.get("FLASK_ENV"),
            release=app.config.get("APP_VERSION", None),
            debug=app.config.get("DEBUG", False),
        )
        print("Sentry initialized for environment: ", f"{app.config.get('FLASK_ENV')}")
    else:
        print("SENTRY_DSN not found. Sentry will not be initialized.")

    # --- Clerk SDK Initialization ---
    clerk_secret_key = app.config.get("CLERK_SECRET_KEY")

    if not clerk_secret_key:
        print("WARNING: CLERK_SECRET_KEY not found. Clerk authentication will be disabled.")
        app.clerk_client = None
    else:
        app.clerk_client = Clerk(bearer_auth=clerk_secret_key)
        print("Clerk SDK initialized successfully.")

    # --- Supabase Client Initialization ---
    supabase_url = app.config.get("SUPABASE_URL")
    supabase_key = app.config.get("SUPABASE_KEY")

    if not supabase_url or not supabase_key:
        print("WARNING: SUPABASE_URL or SUPABASE_KEY not found. Supabase client will not be initialized.")
        app.supabase_client = None
    else:
        app.supabase_client = create_client(supabase_url, supabase_key)
        print("Supabase client initialized successfully.")

    # --- Initialize Flask Extensions (after app config) ---
    cors.init_app(app)

    # --- Register Blueprints ---
    from .routes.main import main_bp
    from .routes.auth import auth_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)

    return app
