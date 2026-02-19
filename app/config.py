# app/config.py
import os


class Config:
    """Base configuration."""

    FLASK_ENV = os.getenv("FLASK_ENV", "development")
    SENTRY_DSN = os.getenv("SENTRY_DSN")
    SENTRY_TRACES_SAMPLE_RATE = float(
        os.getenv("SENTRY_TRACES_SAMPLE_RATE", "1.0")
    )
    SENTRY_PROFILES_SAMPLE_RATE = float(
        os.getenv("SENTRY_PROFILES_SAMPLE_RATE", "1.0")
    )
    APP_VERSION = os.getenv(
        "APP_VERSION", "1.0.0"
    )  # Example for Sentry release tracking

    # Clerk Configuration
    CLERK_SECRET_KEY = os.getenv("CLERK_SECRET_KEY")

    # Supabase Configuration
    SUPABASE_URL = os.getenv("SUPABASE_URL")
    SUPABASE_KEY = os.getenv("SUPABASE_KEY")


class DevelopmentConfig(Config):
    """Development configuration."""

    DEBUG = True
    CORS_HEADERS = "Content-Type"  # Example CORS setting


class ProductionConfig(Config):
    """Production configuration."""

    DEBUG = False
    SENTRY_TRACES_SAMPLE_RATE = float(
        os.getenv("SENTRY_TRACES_SAMPLE_RATE", "0.1")
    )  # Lower sample rate for prod
    SENTRY_PROFILES_SAMPLE_RATE = float(
        os.getenv("SENTRY_PROFILES_SAMPLE_RATE", "0.05")
    )
    # Consider stricter CORS policies for production
    CORS_ORIGINS = ["https://your-frontend-domain.com"]
    CORS_SUPPORTS_CREDENTIALS = True  # If using cookies/auth headers
    CORS_ALLOW_HEADERS = ["Content-Type", "Authorization"]
