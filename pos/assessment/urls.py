from django.urls import path
from . import views


app_name = 'assessment'

urlpatterns = [
    path('', views.CommonView.as_view(), name='common'),
    path('language', views.LanguageView.as_view(), name='language'),
    path('subject', views.SubjectView.as_view(), name='subject'),
    path('exam', views.ExamV2View.as_view(), name='exam'),
    path('downloadassess', views.DownloadView.as_view(), name='downloadassess'),
]
