from django.db import models
from django.db.models import Q
from django.db import transaction
from django.db.utils import IntegrityError

# Create your models here.

class LanguageModelManager(models.Manager):

    def save_language_data(self, language_lst):
        try:
            qs = Language.objects.all().values_list('languageid', 'languagename')
            if not qs.exists():
                obj_list = [Language(**data_dict) for data_dict in language_lst]
                Language.objects.bulk_create(obj_list, ignore_conflicts=True, batch_size=1000)
            elif qs.exists():
                for lst in language_lst:
                    if Language.objects.filter(~Q(languagename=lst['languagename']), languageid=lst['languageid']):
                        qs.filter(~Q(languagename=lst['languagename']), languageid=lst['languageid']).update(languagename=lst['languagename'])
                    else:
                        obj, created = qs.get_or_create(
                            languageid=lst['languageid'],
                            languagename=lst['languagename']
                        )
        except IntegrityError:
            # transaction.rollback()
            return '-1'


class LanguageModel(models.Model):
    languageid = models.CharField(max_length=30)
    languagename = models.CharField(max_length=30)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = LanguageModelManager()

    class Meta:
        abstract = True
        # app_label = 'channels'
        ordering = ['-updated_at']


class Language(LanguageModel):
    pass

