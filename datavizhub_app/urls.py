from django.urls import path
from . import views


urlpatterns = [
   path('', views.dashboard, name='dashboard'),
   path('upload/', views.upload_file, name='upload_file'),
   path('apply_filters/', views.apply_filters, name='apply_filters')
]
