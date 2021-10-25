from django.db import models
from django.db.models import Q
from assessment.models.language_models import Language
from django.db.utils import IntegrityError
import traceback, time


class SubjectModelManager(models.Manager):
    
    def save_subject_data(self, subject_lst, lids):
        try:
            qs = Subject.objects.all().values_list('subjectid', 'subjectname')

            if not qs.exists():
                for lst in subject_lst:
                    obj, created = qs.get_or_create(
                        languageid=lids,
                        subjectid=lst['subjectid'],
                        subjectname=lst['subjectname']
                    )
            elif qs.exists():
                for lst in subject_lst:
                    if Subject.objects.filter(~Q(subjectname=lst['subjectname']), subjectid=lst['subjectid']):
                        qs.filter(~Q(subjectname=lst['subjectname']), subjectid=lst['subjectid']).update(subjectname=lst['subjectname'])
                    else:
                        obj, created = qs.get_or_create(
                            languageid=lids,
                            subjectid=lst['subjectid'],
                            subjectname=lst['subjectname']
                        )
        except IntegrityError as ie:
            traceback.print_exc()
            print("subject integrity error is ", ie)
            return '-1'


class SubjectModel(models.Model):
    # languageId = models.ForeignKey(Language, related_name='languageId', on_delete=models.CASCADE)
    languageid = models.CharField(max_length=30)
    subjectid = models.CharField(max_length=30)
    subjectname = models.CharField(max_length=150)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = SubjectModelManager()

    class Meta:
        abstract = True
        app_label = 'channels'


class Subject(SubjectModel):
    pass
