from django.urls import path
from . import views

urlpatterns = [
    path('process/', views.process, name='process'),
    path('upload/', views.upload, name='upload'),
    path('view/', views.view_data, name='view_data'),
    path('celery/', views.test_celery, name='test_celery'),
    path('get-presigned-url/', views.get_presigned_url, name='get_presigned_url'),
]
