from unicodedata import name
from django.urls import path
from . import views

app_name = 'content_update'


urlpatterns = [
    path('updatecheck/', views.UpdateCheckView.as_view(), name='updatecheck'),
]
