from . import views
from rest_framework import routers
from django.urls import path, include
# from  rest_framework.urlpatterns import format_suffix_patterns


router = routers.DefaultRouter()
router.register('datastore', views.VillageDataStoreView, basename='datastore')
router.register('usagedata', views.UsageDataView, basename='usagedata')
router.register('desktopdata', views.DeskTopDataView, basename='desktopdata')
# for DB Push API
router.register('dbpushdata', views.DbPushDataView, basename='dbpushdata')

urlpatterns = [
    path('', include(router.urls)),
]