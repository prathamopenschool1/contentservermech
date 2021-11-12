import traceback
from django.db import models
from django.db.models import Q
from django.db import transaction
from django.db.utils import IntegrityError

class QuestionModelManager(models.Manager):
    pass


class QuestionModel(models.Model):
    objects = QuestionModelManager()


class Question(QuestionModel):
    pass

class LstQuestionChoiceModel(models.Model):
    lstquestionchoice = models.ForeignKey(Question, related_name='lstquestionchoice', on_delete=models.CASCADE)

