import time
import logging
from django.http import JsonResponse

logger = logging.getLogger(__name__)

class TradingEngineMiddleware:
    """
    MNC-Standard Middleware for Trading Engine.
    Handles:
    1. Request ID tracking
    2. Execution time monitoring
    3. Global exception logging
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Pre-processing
        start_time = time.time()
        
        response = self.get_response(request)

        # Post-processing
        duration = time.time() - start_time
        response['X-Execution-Time'] = f"{duration:.4f}s"
        
        logger.info(f"Path: {request.path} | Method: {request.method} | Duration: {duration:.4f}s")
        
        return response

    def process_exception(self, request, exception):
        import traceback

        print("\n🔥 REAL ERROR BELOW 🔥")
        traceback.print_exc() 

        return JsonResponse({
            "error": str(exception),
        }, status=500)
