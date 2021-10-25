from django.contrib import admin
from .models.language_models import Language
from .models.subject_models import Subject

admin.site.register(Language)
admin.site.register(Subject)
