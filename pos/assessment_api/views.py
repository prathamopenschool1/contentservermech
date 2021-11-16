from django.db.models import query
from rest_framework import viewsets
from rest_framework import pagination
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination

# filters import
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend

#serializers
from .serializers import (LanguageSerializer, SubjectSerializer, ExamSerializer, PaperPatternSerializer, QuestionModelSerializer)

#models
from assessment.models.exam_models import Exam
from assessment.models.subject_models import Subject
from assessment.models.language_models import Language
from assessment.models.pattern_models import PaperPattern
from assessment.models.question_models import QuestionModel, LstQuestionChoiceModel

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


class PaperPatterApiView(viewsets.ModelViewSet):
    queryset = PaperPattern.objects.all()
    serializer_class = PaperPatternSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter)
    filter_fields = ('examid',)
    pagination_class = PageNumberPagination


class QuestionApiView(viewsets.ModelViewSet):
    queryset = QuestionModel.objects.all()
    serializer_class = QuestionModelSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter)
    filter_fields = ('languageid', 'subjectid', 'topicid')
    pagination_class = PageNumberPagination


