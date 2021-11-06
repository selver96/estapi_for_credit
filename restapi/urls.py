from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
    path('', get_application),
    path('create-application/', create_application),
]
