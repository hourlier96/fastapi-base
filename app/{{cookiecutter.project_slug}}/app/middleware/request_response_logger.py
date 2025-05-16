from __future__ import annotations

import time
from typing import Callable

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

from app.core.logging import log


class RequestResponseLoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        start_time = time.time()

        # Read request body (may be empty)
        try:
            request_body_bytes = await request.body()
            request_body = request_body_bytes.decode("utf-8", errors="replace")
        except Exception:
            request_body = "<could not read request body>"

        log.info(
            "Incoming request",
            extra={
                "method": request.method,
                "path": str(request.url.path),
                "query": str(request.url.query),
                "client": request.client.host if request.client else None,
            },
        )

        try:
            response = await call_next(request)

            # Attempt to read response body (works for regular responses)
            response_body = None
            try:
                body_bytes = b""
                async for chunk in response.body_iterator:  # type: ignore[attr-defined]
                    body_bytes += chunk
                response_body = body_bytes.decode("utf-8", errors="replace")

                # Rebuild the response since we've consumed the iterator
                new_response = Response(
                    content=body_bytes,
                    status_code=response.status_code,
                    headers=dict(response.headers),
                    media_type=response.media_type,
                )
            except Exception:
                # If we can't read the body (streaming, etc.), fallback
                new_response = response

            process_time = time.time() - start_time
            log.info(
                "Request handled",
                extra={
                    "status_code": new_response.status_code,
                    "process_time": f"{process_time:.3f}s",
                },
            )

            # Optionally log small bodies (avoid logging huge payloads)
            if request_body:
                log.debug("Request body", extra={"body": request_body[:2000]})
            if response_body:
                log.debug("Response body", extra={"body": response_body[:2000]})

            return new_response

        except Exception as exc:  # pragma: no cover - error path
            log.exception("Exception during request handling")
            raise
