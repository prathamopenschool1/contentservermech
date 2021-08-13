from django.views import View
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from modpush.pushhelper.connectcheck import PushHelper
from .assesshelper import AssesmentHelper
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin


class CommonView(LoginRequiredMixin, TemplateView):
    template_name = "assessment/commonpage.html"


class LanguageView(LoginRequiredMixin, View):
    
    psh = PushHelper()
    ash = AssesmentHelper()

    def get(self, request):
        if self.psh.connect() == True:
            result = self.ash.language_call()
            context = {}
            context['language_result'] = result
            return render(self.request, 'assessment/language.html', context)
        else:
            return render(self.request, 'core/NoInternetFound.html')


class SubjectView(LoginRequiredMixin, View):

    psh = PushHelper()
    ash = AssesmentHelper()

    def get(self, request, langId, langName):
        if self.psh.connect() == True:
            result = self.ash.subject_call(langId)
            context = {}
            context['subject_result'] = result
            context['langName'] = langName
            context['langId'] = langId
            return render(self.request, 'assessment/subject.html', context)
        else:
            return render(self.request, 'core/NoInternetFound.html')


class ExamV2View(LoginRequiredMixin, View):

    psh = PushHelper()
    ash = AssesmentHelper()

    def get(self, request, langName, langId, subjName, subjId):
        if self.psh.connect() == True:
            result = self.ash.exam_call(langId, subjId)
            context = {}
            context['exam_result'] = result[0]['lstsubjectexam']
            context['langName'] = langName
            context['subjName'] = subjName
            context['langId'] = langId
            context['subjId'] = subjId
            return render(self.request, 'assessment/exams.html', context)
        else:
            return render(self.request, 'core/NoInternetFound.html')
    

class DownloadView(LoginRequiredMixin, View):

    def get(self, *args, **kwargs):

        return HttpResponse("this is download view")


