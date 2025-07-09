import httpx
from flask import request, abort, g, current_app
from functools import wraps
from clerk_backend_api.security.types import AuthenticateRequestOptions


def clerk_required(f):
    """
    Modern Clerk decorator using the official authenticate_request method
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        clerk_client = current_app.clerk_client
        if not clerk_client:
            abort(500, description="Clerk SDK not initialized")

        # Convert Flask request to httpx.Request
        print(f"REQUEST HEADERS {request.headers}")
        httpx_request = httpx.Request(
            method=request.method,
            url=str(request.url),
            headers=dict(request.headers),
            content=request.get_data()
        )
        print(f"httpx_request {httpx_request.headers}")

        try:
            # Use Clerk's built-in authentication
            request_state = clerk_client.authenticate_request(
                httpx_request,
                AuthenticateRequestOptions(
                    # Add your authorized parties (your frontend URLs)
                    authorized_parties=[
                        'http://localhost:3000',  # Development frontend
                        'https://yourdomain.com'   # Production frontend
                    ]
                )
            )

            if not request_state.is_signed_in:
                abort(401, description="Authentication required")

            # Set user context from the request state
            g.clerk_user_id = request_state.user_id
            g.clerk_session_id = request_state.session_id
            g.clerk_request_state = request_state
            
            # You can also access more details:
            # g.clerk_user = request_state.user  # Full user object
            # g.clerk_session = request_state.session  # Full session object
            
        except Exception as e:
            print(f"Authentication error: {e}")
            abort(500, description="Authentication error occurred")

        return f(*args, **kwargs)

    return decorated_function