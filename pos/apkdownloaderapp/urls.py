from django.urls import path
from . import views

app_name = 'apkdownloaderapp'

urlpatterns = [
    path("apkdwn/", views.apk_index, name="apkdwn"),
]

