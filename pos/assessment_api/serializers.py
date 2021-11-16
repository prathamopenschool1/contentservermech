from django.db import models
from django.db.models import fields
from rest_framework import serializers
from assessment.models.subject_models import Subject
from assessment.models.language_models import Language
from assessment.models.exam_models import Exam, LstSubjectExamModel
from assessment.models.pattern_models import PaperPattern, LstExamCertificateTopicListModel, LstPatternDetailModel
from  assessment.models.question_models import LstQuestionChoiceModel, QuestionModel


class LanguageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Language
        fields = ['languageid', 'languagename']


class SubjectSerializer(serializers.ModelSerializer):

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


class LstPatternDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = LstPatternDetailModel
        fields = ['topicid', 'topicname','qtid','qtname','qlevel','totalmarks','noofquestion','marksperquestion','qlevelmarks','paralevel','keyworddetail']


class LstExamCertificateTopicListSerializer(serializers.ModelSerializer):

    class Meta:
        model = LstExamCertificateTopicListModel
        fields = ['certificatequestion', 'certificatekeyword']


class PaperPatternSerializer(serializers.ModelSerializer):
    lstpatterndetail = LstPatternDetailSerializer(many=True, read_only=True)
    lstexamcertificatetopiclist = LstExamCertificateTopicListSerializer(many=True, read_only=True)

    class Meta:
        model = PaperPattern
        fields = ['subjectid', 'subjectname', 'examid', 'examname', 'examduration', 'question1', 'question2', 'question3', 'question4', 'question5', 'question6', 'question7', 'question8', 'question9', 'question10', 'IsRandom', 'noofcertificateq', 'exammode', 'examtype', 'outofmarks', 'lstpatterndetail', 'lstexamcertificatetopiclist']



class LstQuestionChoiceModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = LstQuestionChoiceModel
        fields = ['qid', 'qcid', 'matchingname', 'choicename', 'correct', 'matchingurl', 'choiceurl', 'AppVersionChoice', 'localChoiceUrl', 'localMatchUrl']


class QuestionModelSerializer(serializers.ModelSerializer):
    lstquestionchoice = LstQuestionChoiceModelSerializer(many=True, read_only=True)
    class Meta:
        model = QuestionModel
        fields = ['qid', 'languageid' ,'subjectid' ,'topicid' ,'lessonid' ,'qtid' ,'qname' ,'answer' ,'photourl' ,'ansdesc' ,'qlevel' ,'hint' ,'addedby' ,'addedtime' ,'updatedby' ,'updatedtime' ,'IsParaQuestion' ,'RefParaID' ,'isdeleted' ,'AppVersion' ,'localPhotoUrl', 'lstquestionchoice']
