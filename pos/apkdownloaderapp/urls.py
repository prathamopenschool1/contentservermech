from django.urls import path
from . import views

app_name = 'apkdownloaderapp'


urlpatterns = [
    path('apkdwn/', views.ApkPageServeView.as_view(), name='apkdwn'),
    path('checkInternetCon/', views.ApkDownloadView.as_view(), name='checkInternetCon'),
]


