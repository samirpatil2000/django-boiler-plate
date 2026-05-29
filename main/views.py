import time
from datetime import datetime, timezone
from django.http import JsonResponse

START_TIME = time.time()

def convert_seconds_to_hms(seconds):
    """Convert seconds to days, hours, minutes, seconds format"""
    days = int(seconds // 86400)
    hours = int((seconds % 86400) // 3600)
    minutes = int((seconds % 3600) // 60)
    seconds = int(seconds % 60)
    
    if days > 0:
        return f"{days}d {hours}h {minutes}m {seconds}s"
    return f"{hours}h {minutes}m {seconds}s"

def health_check(request):
    uptime_seconds = time.time() - START_TIME
    health_check_response = {
        "status": "UP",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "uptime": convert_seconds_to_hms(uptime_seconds),
    }
    return JsonResponse(health_check_response)
