from django.urls import path
from . import views

urlpatterns = [
    path('hello/', views.hello_view),
    path('health/', views.health_check),
    path('location/', views.get_city_weather),
]