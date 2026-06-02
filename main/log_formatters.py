import json
import logging
from datetime import datetime, timezone, timedelta
from main.logging_context import request_var, trace_id_var, user_id_var

class RequestContextFilter(logging.Filter):
    """Enriches log records with active context variables."""
    def filter(self, record):
        record.traceId = trace_id_var.get() or '-'
        
        request = request_var.get()
        if request:
            record.method = request.method
            record.path = request.path
            if hasattr(request, "user") and request.user and request.user.is_authenticated:
                record.userId = request.user.id
            else:
                record.userId = user_id_var.get() or 'anonymous'
        else:
            record.method = '-'
            record.path = '-'
            record.userId = user_id_var.get() or 'anonymous'
        return True

class JSONFormatter(logging.Formatter):
    """Formats log records into single-line JSON structures."""
    def format(self, record):
        # Localize time (UTC+5:30)
        ist_tz = timezone(timedelta(hours=5, minutes=30))
        ist_time = datetime.now(ist_tz)
        
        log_data = {
            "level": record.levelname.lower(),
            "ts": ist_time.isoformat(),
            "msg": record.getMessage(),
            "platform": "django-app",
            "traceId": getattr(record, "traceId", "-"),
            "userId": getattr(record, "userId", "anonymous"),
            "method": getattr(record, "method", "-"),
            "path": getattr(record, "path", "-"),
        }

        # Pull custom keywords passed in extra=
        for key in ["process_time", "status_code", "data"]:
            val = getattr(record, key, None)
            if val is not None:
                log_data[key] = val

        # Handle exception tracebacks
        if record.exc_info:
            log_data["exception"] = self.formatException(record.exc_info)

        return json.dumps(log_data)
