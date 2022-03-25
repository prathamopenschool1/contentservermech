from django.urls import path
from . import views

app_name = 'apkdownloaderapp'


urlpatterns = [
    path('apkdwn/', views.ApkDownloadView.as_view(), name='apkdwn')
]


