from django.urls import path
from .views import base, registro
urlpatterns = [
    path('', base, name='base'),
    path('registro/', registro, name="registro"),
]