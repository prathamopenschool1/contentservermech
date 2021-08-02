from django.urls import path
from . import views

urlpatterns = [
    path('', views.assindex, name='index'),
]
