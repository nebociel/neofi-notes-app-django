from django.contrib import admin
from django.urls import include, path
from rest_framework.response import Response


def not_found(request, *args, **kwargs):
    error_response = {'error': 'The requested URL was not found.'}
    return Response(error_response, status=404)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('notes.urls')),
    path('<path:path>/', not_found),
]
