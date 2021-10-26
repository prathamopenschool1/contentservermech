import traceback
from django.db import models
from django.db.models import Q
from django.db import transaction
from django.db.utils import IntegrityError


class PaperPatternModelManager(models.Manager):
    pass


class PaperPatternModel(models.Model):
    subjectid = models.CharField(max_length=50)
    subjectname
    examid
    examname
    examduration
    question1
    question2
    question3
    question4
    question5
    question6
    question7
    question8
    question9
    question10
    IsRandom
    noofcertificateq
    exammode
    examtype
    outofmarks
    objects = PaperPatternModelManager()



class PaperPattern(PaperPatternModel):
    pass



