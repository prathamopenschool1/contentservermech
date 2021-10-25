from django.db import models
from django.db.models import fields
from rest_framework import serializers
from assessment.models.exam_models import Exam, LstSubjectExamModel
from assessment.models.subject_models import Subject
from assessment.models.language_models import Language


class LanguageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Language
        fields = ['languageid', 'languagename']


class SubjectSerializer(serializers.ModelSerializer):
    # languageId = LanguageSerializer(many=True)

    class Meta:
        model = Subject
        fields = ['subjectid', 'subjectname', 'languageid']

class LstSubjectExamSerializer(serializers.ModelSerializer):

    class Meta:
        model = LstSubjectExamModel
        fields = ['examid', 'examname', 'exammode', 'examtype', 'languageid', 'languagename', 'lstexampaper']



class ExamSerializer(serializers.ModelSerializer):
    lstsubjectexam = LstSubjectExamSerializer(many=True, read_only=True)

    class Meta:
        model = Exam
        fields = ['subjectid', 'subjectname', 'languageid', 'lstsubjectexam']
