import traceback
from django.db import models
from django.db.models import Q
from django.db import transaction
from django.db.utils import IntegrityError


class PaperPatternModelManager(models.Manager):
    
    def save_pattern_data(self, pattern_result, eids):
        try:
            obj, created = PaperPattern.objects.get_or_create(
                subjectid        = pattern_result['subjectid'],
                subjectname      = pattern_result['subjectname'], 
                examid           = pattern_result['examid'],
                examname         = pattern_result['examname'],
                examduration     = pattern_result['examduration'],
                question1        = pattern_result['question1'],
                question2        = pattern_result['question2'],
                question3        = pattern_result['question3'],
                question4        = pattern_result['question4'],
                question5        = pattern_result['question5'],
                question6        = pattern_result['question6'],
                question7        = pattern_result['question7'],
                question8        = pattern_result['question8'],
                question9        = pattern_result['question9'],
                question10       = pattern_result['question10'],
                IsRandom         = pattern_result['IsRandom'],
                noofcertificateq = pattern_result['noofcertificateq'],
                exammode         = pattern_result['exammode'],
                examtype         = pattern_result['examtype'],
                outofmarks       = pattern_result['outofmarks']
                
            )
            for lst in pattern_result['lstpatterndetail']:
                lobj, lcreated = LstPatternDetailModel.objects.get_or_create(
                    paper_pattern       = obj,
                    topicid             = lst['topicid'],
                    topicname           = lst['topicname'], 
                    qtid                = lst['qtid'],
                    qtname              = lst['qtname'],
                    qlevel              = lst['qlevel'],
                    totalmarks          = lst['totalmarks'],
                    noofquestion        = lst['noofquestion'],
                    marksperquestion    = lst['marksperquestion'],
                    qlevelmarks         = lst['qlevelmarks'],
                    paralevel           = lst['paralevel'],
                    keyworddetail       = lst['keyworddetail']
                )
            
            for data in pattern_result['lstexamcertificatetopiclist']:
                dobj, dcreated = LstExamCertificateTopicListModel.objects.get_or_create(
                    paperPattern        = obj,
                    certificatequestion = data['certificatequestion'],
                    certificatekeyword  = data['certificatekeyword']
                )
           
        except IntegrityError as ier:
            print("pattern error is >> ", ier)
            return '-1'


class PaperPatternModel(models.Model):
    subjectid = models.IntegerField()
    subjectname = models.CharField(max_length=255)
    examid = models.IntegerField()
    examname = models.CharField(max_length=255)
    examduration = models.CharField(max_length=255)
    question1  = models.CharField(max_length=255, blank=True, null=True)
    question2  = models.CharField(max_length=255, blank=True, null=True)
    question3  = models.CharField(max_length=255, blank=True, null=True)
    question4  = models.CharField(max_length=255, blank=True, null=True)
    question5  = models.CharField(max_length=255, blank=True, null=True)
    question6  = models.CharField(max_length=255, blank=True, null=True)
    question7  = models.CharField(max_length=255, blank=True, null=True)
    question8  = models.CharField(max_length=255, blank=True, null=True)
    question9  = models.CharField(max_length=255, blank=True, null=True)
    question10 = models.CharField(max_length=255, blank=True, null=True)
    IsRandom = models.BooleanField(default=False)
    noofcertificateq = models.IntegerField()
    exammode = models.CharField(max_length=50)
    examtype = models.CharField(max_length=50)
    outofmarks = models.IntegerField()

    objects = PaperPatternModelManager()

    class Meta:
        abstract = True



class PaperPattern(PaperPatternModel):
    pass



class LstPatternDetailModel(models.Model):
    paper_pattern = models.ForeignKey(PaperPattern, related_name='lstpatterndetail',on_delete=models.CASCADE)
    topicid = models.IntegerField()
    topicname   = models.CharField(max_length=255, blank=True, null=True)
    qtid    = models.IntegerField()
    qtname  = models.CharField(max_length=255, blank=True, null=True)
    qlevel  = models.CharField(max_length=100, blank=True, null=True)
    totalmarks  = models.IntegerField()
    noofquestion    = models.IntegerField()
    marksperquestion    = models.IntegerField()
    qlevelmarks = models.IntegerField()
    paralevel   = models.IntegerField()
    keyworddetail   = models.CharField(max_length=255, blank=True, null=True)


    # class Meta:
    #     app_label = 'channels'

    
    @classmethod
    def create(cls, topicid, topicname, qtid, qtname, qlevel, totalmarks, noofquestion,  marksperquestion, qlevelmarks, paralevel, keyworddetail):
        lst_pattern_data = cls(topicid=topicid, topicname=topicname, qtid=qtid, qtname=qtname, qlevel=qlevel, totalmarks=totalmarks, noofquestion=noofquestion,  marksperquestion=marksperquestion, qlevelmarks=qlevelmarks, paralevel=paralevel, keyworddetail=keyworddetail)

        return lst_pattern_data


    def __str__(self):
        return str(self.topicid)
    


class LstExamCertificateTopicListModel(models.Model):
    paper_pattern = models.ForeignKey(PaperPattern, related_name='lstexamcertificatetopiclist', on_delete=models.CASCADE)
    certificatequestion = models.TextField(blank=True, null=True)
    certificatekeyword  = models.TextField(blank=True, null=True)

    # class Meta:
    #     app_label = 'channels'

    @classmethod
    def create(cls, certificatequestion, certificatekeyword):
        lst_exam_certificate_data = cls(certificatequestion=certificatequestion, certificatekeyword=certificatekeyword)

        return lst_exam_certificate_data


    # def __str__(self):
    #     return self.certificatequestion
    


