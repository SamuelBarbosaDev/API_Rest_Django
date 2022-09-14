from . import views
from django.urls import path, include
from rest_framework import routers
from core.api import viewsets

route = routers.DefaultRouter()
route.register(r'api-auth', viewsets.ClienteSerializer, basename='api-auth')

urlpatterns = [
    path('base', views.base, name='base'),
    path('', include(route.urls), name='api')
]
