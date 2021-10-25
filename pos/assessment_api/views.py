from django.db.models import query
from rest_framework import viewsets
from rest_framework import pagination
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination

# filters import
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend

#serializers
from .serializers import (LanguageSerializer, SubjectSerializer, ExamSerializer)

#models
from assessment.models.exam_models import Exam
from assessment.models.subject_models import Subject
from assessment.models.language_models import Language

from assessment_api import serializers

class LanguageApiView(viewsets.ModelViewSet):
    queryset = Language.objects.all()
    serializer_class = LanguageSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter)
    filter_fields = ('languageid',)
    pagination_class = PageNumberPagination


class SubjectApiView(viewsets.ModelViewSet):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter)
    filter_fields = ('languageid',)
    pagination_class = PageNumberPagination


class ExamApiView(viewsets.ModelViewSet):
    queryset = Exam.objects.all()
    serializer_class = ExamSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter)
    filter_fields = ('languageid', 'subjectid')
    pagination_class = PageNumberPagination
