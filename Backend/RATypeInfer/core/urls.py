from django.urls import path
from . import views

urlpatterns = [
    path('process/', views.process, name='process'),
    path('upload/', views.upload, name='upload'),
    path('view/', views.view_data, name='view_data'),
]
