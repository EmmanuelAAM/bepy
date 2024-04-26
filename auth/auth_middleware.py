from auth.auth_utils import decode_token
from fastapi import Request, status
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from typing import Optional

# Check the authentication status in every request made to the api
# with the exeption of those made to the authentication endpoint
class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # List of paths that don't require authentication
        exempt_paths = ["/auth/"]
        if request.url.path not in exempt_paths:
            authorization = request.headers.get('Authorization')
            if not authorization:
                return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content={"message": "Missing Authorization"})
            token_type, _, token = authorization.partition(' ')
            if token_type.lower() != 'bearer' or not token:
                return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content={"message": "Invalid or missing Token"})
            try:
                payload = decode_token(token)
            except:
                return JSONResponse(status_code=status.HTTP_403_FORBIDDEN, content={"message": "Not authorized"})
            username: Optional[str] = payload.get("sub")
            request.state.token = token
            request.state.username = username
            if not username:
                return JSONResponse(status_code=status.HTTP_403_FORBIDDEN, content={"message": "Not authorized"})
        response = await call_next(request)
        return response
