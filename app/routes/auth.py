from flask import Blueprint, jsonify, g

from ..auth.decorators import clerk_required
from ..auth.helpers import get_current_user

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")


@auth_bp.route("/protected")
@clerk_required
def protected_route():
    """Protected route using the decorator"""
    return jsonify(
        {
            "message": f"Welcome, user {g.clerk_user_id}!",
            "user_id": g.clerk_user_id,
            "session_id": g.clerk_session_id,
        }
    )


@auth_bp.route("/user")
def user_info():
    """Route that works with or without auth"""
    user = get_current_user()
    if user:
        return jsonify(
            {
                "authenticated": True,
                "user_id": user["user_id"],
                "email": (
                    user["user"].email_addresses[0].email_address
                    if user["user"].email_addresses
                    else None
                ),
            }
        )
    else:
        return jsonify({"authenticated": False})


@auth_bp.route("/me")
@clerk_required
def get_user_details():
    """Get detailed user information"""
    # Access full user object from request state
    user = g.clerk_request_state.user
    session = g.clerk_request_state.session

    return jsonify(
        {
            "user_id": user.id,
            "email": (
                user.email_addresses[0].email_address if user.email_addresses else None
            ),
            "first_name": user.first_name,
            "last_name": user.last_name,
            "session_id": session.id,
            "last_active": session.last_active_at,
        }
    )
