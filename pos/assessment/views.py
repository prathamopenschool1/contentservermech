import json
from django.views import View
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from modpush.pushhelper.connectcheck import PushHelper
from .assesshelper import AssesmentHelper
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin


class CommonView(LoginRequiredMixin, TemplateView):
    template_name = "assessment/assessmentpage.html"


class LanguageView(LoginRequiredMixin, View):
    
    psh = PushHelper()
    ash = AssesmentHelper()

    def post(self, request):
        if self.psh.connect() == True:
            result = self.ash.language_call()
            if result['status'] == 200:
                context = {}
                context['language_result'] = result['lang_result']
                # return render(self.request, 'assessment/language.html', context)
                return JsonResponse(context, safe=False)
            else:
                context = {}
                context['msg'] = "Something Went Wrong!! Please Check Internet Connection"
                context['status'] = 404
                return JsonResponse(context, safe=False)
        else:
            return render(self.request, 'core/NoInternetFound.html')


class SubjectView(LoginRequiredMixin, View):

    psh = PushHelper()
    ash = AssesmentHelper()

    def post(self, request, *args, **kwargs):
        posted_data = json.loads(request.body.decode("utf-8"))
        langId = posted_data['langId']
        langName = posted_data['langName']
        if self.psh.connect() == True:
            result = self.ash.subject_call(langId)
            if result['status'] == 200:
                context = {}
                context['subject_result'] = result
                # context['langName'] = langName
                # context['langId'] = langId
                # return render(self.request, 'assessment/subject.html', context)
                return JsonResponse(context, safe=False)
            else:
                context = {}
                context['msg'] = "Something Went Wrong!! Please Check Internet Connection"
                context['status'] = 404
                return JsonResponse(context, safe=False)
        else:
            return render(self.request, 'core/NoInternetFound.html')


class ExamV2View(LoginRequiredMixin, View):

    psh = PushHelper()
    ash = AssesmentHelper()

    def post(self, request):
        posted_exam_data = json.loads(request.body.decode("utf-8"))
        languageid = posted_exam_data['languageid']
        # langName = posted_exam_data['langName']
        subjectid = posted_exam_data['subjectid']
        # subjName = posted_exam_data['subjName']
        if self.psh.connect() == True:
            result = self.ash.exam_call(languageid, subjectid)
            if result['status'] == 200:
                context = {}
                context['exam_result'] = result
                # context['langName'] = langName
                # context['subjName'] = subjName
                context['languageid'] = languageid
                context['subjectid'] = subjectid
                return JsonResponse(context, safe=False)
        else:
            return render(self.request, 'core/NoInternetFound.html')
    

class DownloadView(LoginRequiredMixin, View):

    psh = PushHelper()
    ash = AssesmentHelper()

    def post(self, request, *args, **kwargs):
        asessment_array_data = json.loads(request.body.decode("utf-8"))
        languageIds = asessment_array_data['languageid']
        subjectIds = asessment_array_data['subjectid']
        examIds = asessment_array_data['examid']
        if self.psh.connect() == True:
            result = self.ash.pattern_call(examIds)
            print("my lst result >>>>>>>>>>>>>>>>>>>>>>>>>>>> ")
            print("results >>>> ", result)
            if result['status'] == 200:
                quesPatternDetails = self.ash.question_details(languageIds, result['exam_pattern'])
            context = {}
            context['languageIds'] = languageIds
            context['subjectIds'] = subjectIds
            context['exexamIds'] = examIds
            # print(context)
        return JsonResponse(context, safe=False)


