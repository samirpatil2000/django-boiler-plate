import uuid
import time
import logging
from django.utils.deprecation import MiddlewareMixin
from main.logging_context import request_var, trace_id_var, user_id_var

logger = logging.getLogger("django.request")

class DjangoLoggingMiddleware(MiddlewareMixin):
    def process_request(self, request):
        # 1. Extract or generate Trace ID
        trace_id = request.headers.get("X-Trace-ID") or request.META.get("HTTP_X_TRACE_ID") or str(uuid.uuid4())
        request.trace_id = trace_id
        
        # 2. Extract User Context
        user_id = request.user.id if hasattr(request, "user") and request.user and request.user.is_authenticated else "anonymous"

        # 3. Store in ContextVars (Save tokens for cleanup)
        request.request_token = request_var.set(request)
        request.trace_token = trace_id_var.set(trace_id)
        request.user_token = user_id_var.set(user_id)
        
        # 4. Measure request start
        request.start_time = time.time()

    def process_response(self, request, response):
        # 1. Log request completion details
        if hasattr(request, "start_time"):
            duration = round((time.time() - request.start_time) * 1000, 2)
            logger.info(
                f"Request completed: {request.method} {request.path} -> {response.status_code} in {duration}ms",
                extra={
                    "process_time": duration,
                    "status_code": response.status_code,
                }
            )

        # 2. Inject X-Trace-ID into response header
        if hasattr(request, "trace_id"):
            response["X-Trace-ID"] = request.trace_id

        # 3. Clear ContextVars to prevent leakage
        self._cleanup_context(request)
        return response

    def process_exception(self, request, exception):
        # Log uncaught errors with context
        if hasattr(request, "start_time"):
            duration = round((time.time() - request.start_time) * 1000, 2)
            logger.error(
                f"Uncaught exception processing {request.method} {request.path}: {str(exception)}",
                exc_info=True,
                extra={
                    "process_time": duration,
                    "status_code": 500,
                }
            )
        self._cleanup_context(request)

    def _cleanup_context(self, request):
        if hasattr(request, "request_token"):
            try:
                request_var.reset(request.request_token)
            except ValueError:
                pass
        if hasattr(request, "trace_token"):
            try:
                trace_id_var.reset(request.trace_token)
            except ValueError:
                pass
        if hasattr(request, "user_token"):
            try:
                user_id_var.reset(request.user_token)
            except ValueError:
                pass
