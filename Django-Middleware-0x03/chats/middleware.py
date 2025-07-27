import logging
from datetime import datetime
from django.http import HttpResponseForbidden

logging.basicConfig(
    filename='requests.log',
    level=logging.INFO,
    format='%(message)s'
)

class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        
    def __call__(self, request):
        path = request.path
        user = request.user.username if request.user.is_authenticated else "Anonymous"
        
        log_message = f"{datetime.now()} - User: {user} - Path: {request.path}"
        logging.info(log_message)
        
        return self.get_response(request)
    
class RestrictAccessByTimeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        
    def __call__(self, request):
        current_hour = datetime.now().hour
        
        if current_hour < 18 or current_hour >= 21:
            return HttpResponseForbidden("Access is only allowed between 6pm or 9pm.")
        
        return self.get_response(request)