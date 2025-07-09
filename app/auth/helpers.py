import httpx
from flask import request, current_app
from clerk_backend_api.security.types import AuthenticateRequestOptions


def get_current_user():
    """
    Helper function to get current user info in any route
    """
    clerk_client = current_app.clerk_client
    if not clerk_client:
        return None

    httpx_request = httpx.Request(
        method=request.method,
        url=str(request.url),
        headers=dict(request.headers),
        content=request.get_data(),
    )

    try:
        request_state = clerk_client.authenticate_request(
            httpx_request,
            AuthenticateRequestOptions(
                authorized_parties=["http://localhost:3000", "https://yourdomain.com"]
            ),
        )

        if request_state.is_signed_in:
            return {
                "user_id": request_state.user_id,
                "session_id": request_state.session_id,
                "user": request_state.user,
                "session": request_state.session,
            }
    except Exception as e:
        print(f"Error getting current user: {e}")

    return None
