from urllib.parse import urlencode
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

class FlattenQueryStringListMiddleware(BaseHTTPMiddleware):
    def __init__(self, app):
        super().__init__(app)

    async def dispatch(self, request: Request, call_next):
        flattened = []
        for key, value in request.query_params.multi_items():
            flattened.extend((key, entry) for entry in value.split(','))

        request.scope["query_string"] = urlencode(flattened, doseq=True).encode("utf-8")

        response = await call_next(request)
        return response

