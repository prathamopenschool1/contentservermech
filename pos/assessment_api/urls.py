from django.urls import path, include
from rest_framework import routers, urlpatterns
from . import views

router = routers.DefaultRouter()
router.register('GetLanguage', views.LanguageApiView, basename='GetLanguage')
router.register('GetSubjectv2', views.SubjectApiView, basename='GetSubjectv2')
router.register('GetExamV2', views.ExamApiView, basename='GetExamV2')


urlpatterns = [
    path('', include(router.urls)),
]
