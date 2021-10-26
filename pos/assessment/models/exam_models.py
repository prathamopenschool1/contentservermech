import traceback
from django.db import models
from django.db.models import Q
from django.db import transaction
from django.db.utils import IntegrityError

class ExamModelManager(models.Manager):

    def save_exam_data(self, exam_lst, lids, sids):
        try:
            qs = Exam.objects.all()

            for lst in exam_lst:
                obj, created = qs.get_or_create(
                    languageid=lids,
                    subjectid=lst['subjectid'],
                    subjectname=lst['subjectname']
                )

                for data in lst['lstsubjectexam']:
                    eobj, ecreated = LstSubjectExamModel.objects.get_or_create(
                        lstsubjectexam  = obj,
                        examid          = data['examid'],
                        examname        = data['examname'],
                        exammode        = data['exammode'],
                        examtype        = data['examtype'],
                        languageid      = data['languageid'],
                        languagename    = data['languagename'],
                        lstexampaper    = data['lstexampaper']
                    )
                    # if not LstSubjectExamModel.objects.filter(examid=examid, examtype=examtype, languageid=languageid).exists():
                    #     lst_exam_data = LstSubjectExamModel.objects.create(lstsubjectexam=obj, examid=examid, examname=examname, exammode=exammode, examtype=examtype, languageid=languageid, languagename=languagename, lstexampaper=lstexampaper)

                    #     lst_exam_data.save()
        except IntegrityError as ie:
            traceback.print_exc()
            print("Exam integrity error is ", ie)
            return '-1'


class ExamModel(models.Model):
    languageid = models.CharField(max_length=50)
    subjectid = models.CharField(max_length=100)
    subjectname = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = ExamModelManager()

    class Meta:
        abstract = True
        app_label = 'channels'


class Exam(ExamModel):
    pass


class LstSubjectExamModel(models.Model):
    lstsubjectexam  = models.ForeignKey(Exam, related_name='lstsubjectexam', on_delete=models.CASCADE)
    examid          = models.CharField(max_length=100, blank=True, null=True)   
    examname        = models.CharField(max_length=100, blank=True, null=True)
    exammode        = models.CharField(max_length=100, blank=True, null=True)
    examtype        = models.CharField(max_length=100, blank=True, null=True)
    languageid      = models.CharField(max_length=100, blank=True, null=True)
    languagename    = models.CharField(max_length=100, blank=True, null=True)
    lstexampaper    = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        app_label = 'channels'

    
    @classmethod
    def create(cls, examid, examname, exammode, examtype, languageid, languagename, lstexampaper):
        lst_subject_exam_data = cls(examid=examid, examname=examname, exammode=exammode, examtype=examtype, languageid=languageid, languagename=languagename, lstexampape=lstexampaper)
        
        return lst_subject_exam_data


    def __str__(self):
        return str(self.examid)
    
