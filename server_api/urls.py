from django.urls import path
from .views import home, processBet

urlpatterns = [
    path('', home),
    path('api/test', processBet)
]
