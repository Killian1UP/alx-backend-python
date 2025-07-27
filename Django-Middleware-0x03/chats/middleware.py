import logging
from datetime import datetime, timedelta
from django.http import HttpResponseForbidden
from collections import defaultdict
from chats.models import UserRole

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
    
class OffensiveLanguageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.requests_log = defaultdict(list)
        
    def __call__(self, request):
        if request.method == "POST" and request.path.startswith("/api/messages/"):
            ip = self.get_client_ip(request)
            now = datetime.now()
            one_minute_ago = now - timedelta(minutes=1)   
            
            # Clean up old timestamps
            self.requests_log[ip] = [
                ts for ts in self.requests_log[ip] if ts > one_minute_ago
            ]

            if len(self.requests_log[ip]) >= 5:
                return HttpResponseForbidden("Rate limit exceeded: Max 5 messages per minute.")

            self.requests_log[ip].append(now)

        return self.get_response(request) 
    
    def get_client_ip(self, request):
        # If behind a proxy like NGINX, use HTTP_X_FORWARDED_FOR
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            return x_forwarded_for.split(',')[0]
        return request.META.get('REMOTE_ADDR')   
    
class RolepermissionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response     
        
    def __call__(self, request):
        # Restrict access to /api/messages/* for non-admins
        if request.path.startswith("/api/messages/"):
            user = request.user

            if not user.is_authenticated or user.role != UserRole.ADMIN:
                return HttpResponseForbidden("Access denied: Admins only.")

        return self.get_response(request)