from flask import Blueprint, jsonify, current_app

main_bp = Blueprint("main", __name__)


# Health check endpoint
@main_bp.route("/health")
def health():
    supabase_status = "not initialized"
    if hasattr(current_app, "supabase_client") and current_app.supabase_client is not None:
        try:
            # Simple query to verify connection
            current_app.supabase_client.table("_health_check").select("*").limit(1).execute()
            supabase_status = "connected"
        except Exception as e:
            # Connection works even if table doesn't exist
            if "does not exist" in str(e) or "relation" in str(e):
                supabase_status = "connected"
            else:
                supabase_status = f"error: {e}"

    clerk_status = "not initialized"
    if hasattr(current_app, "clerk_client") and current_app.clerk_client is not None:
        clerk_status = "initialized"

    return (
        jsonify(
            {
                "status": "healthy",
                "message": "Flask backend is running",
                "supabase": supabase_status,
                "clerk_sdk": clerk_status,
                "version": current_app.config.get("APP_VERSION", "unknown"),
                "environment": current_app.config.get("FLASK_ENV", "unknown"),
            }
        ),
        200,
    )


# Basic route
@main_bp.route("/")
def index():
    return jsonify(
        {
            "message": "Flask backend API",
            "version": current_app.config.get("APP_VERSION", "unknown"),
        }
    )


# Sentry Test Route (for demonstration purposes, remove in production)
@main_bp.route("/sentry-test")
def sentry_test():
    _ = 1 / 0
    return "This should not be reached if Sentry captures the error."
