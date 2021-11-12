import traceback
from django.db import models
from django.db.models import Q
from django.db import transaction
from django.db.utils import IntegrityError

class QuestionModelManager(models.Manager):
    
    def save_question_data(self, quest_result, localChoice=None, localMatch=None, localPhoto=None):

        pass


class QuestionModel(models.Model):
    qid                 = models.IntegerField(default=0)
    languageid          = models.IntegerField(default=0)
    subjectid           = models.IntegerField(default=0)
    topicid             = models.IntegerField(default=0)
    lessonid            = models.IntegerField(default=0)
    qtid                = models.IntegerField(default=0)
    qname               = models.TextField(default="")
    answer              = models.TextField(default="")
    photourl            = models.TextField(default="")
    ansdesc             = models.TextField(default="")
    qlevel              = models.CharField(max_length=255, default="")
    hint                = models.CharField(max_length=255, default="")
    addedby             = models.IntegerField(default=0)
    addedtime           = models.CharField(max_length=255, default="")
    updatedby           = models.IntegerField(default=0)
    updatedtime         = models.CharField(max_length=255, default="")
    IsParaQuestion      = models.BooleanField(default=False)
    RefParaID           = models.IntegerField(default=0)
    isdeleted           = models.BooleanField(default=False)
    AppVersion          = models.CharField(max_length=255, default="")
    localPhotoUrl       = models.TextField(default="")

    # objects = QuestionModelManager()

    class Meta:
        abstract = True


class Question(QuestionModel):
    pass

class LstQuestionChoiceModel(models.Model):
    lstquestionchoice       = models.ForeignKey(Question, related_name='lstquestionchoice', on_delete=models.CASCADE, blank=True, null=True)
    qid                     = models.IntegerField(default=0)
    qcid                    = models.IntegerField(default=0)
    matchingname            = models.CharField(max_length=255, default="")
    choicename              = models.CharField(max_length=255, default="")
    correct                 = models.BooleanField(default=False)
    matchingurl             = models.TextField(default="")
    choiceurl               = models.TextField(default="")
    AppVersionChoice        = models.CharField(max_length=255, default="")
    localChoiceUrl          = models.TextField(default="")
    localMatchUrl           = models.TextField(default="")


    @classmethod
    def create(cls, qid, qcid, matchingname, choicename, correct, matchingurl, choiceurl, AppVersionChoice):
        lstquestionchoice_data = cls(qid=qid, qcid=qcid, matchingname=matchingname, choicename=choicename, correct=correct, matchingurl=matchingurl, choiceurl=choiceurl, AppVersionChoice=AppVersionChoice)

        return lstquestionchoice_data


    def __str__(self):
        return str(self.qid)
    
