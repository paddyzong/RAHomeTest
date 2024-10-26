from django.urls import path
from . import views

urlpatterns = [
    path('process/',views.process),
    path('upload/',views.upload),
]
