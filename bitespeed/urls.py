from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse

def index(request):
    return JsonResponse({"message": "API is working!"})

urlpatterns = [
    path('', index),
    path('admin/', admin.site.urls),
    path('identify', include('identity.urls')),
]
