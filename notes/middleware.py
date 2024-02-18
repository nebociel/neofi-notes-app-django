from django.http import JsonResponse
from rest_framework.views import exception_handler


class GlobalErrorHandlerMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_exception(self, request, exception):
        error_response = {'error': 'An unexpected error occurred.'}
        return JsonResponse(error_response, status=500)
