from django.urls import path
from . import  views

app_name = 'push'


urlpatterns = [
    path('', views.PushDataView.as_view(), name="push-data"),
    path('usage', views.PushUsageDataView.as_view(), name='usage'),
    path('dbpush', views.DbPushDataView.as_view(), name="dbpush"),
    path('desktop', views.DeskTopDataToServerView.as_view(), name="desktop"),
    path('backup', views.BackUpDataView.as_view(), name="backup"),
    path('clear', views.ClearDataView.as_view(), name="clear"),
]

