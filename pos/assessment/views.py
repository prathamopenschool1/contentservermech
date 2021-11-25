import json
from django.views import View
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from modpush.pushhelper.connectcheck import PushHelper
from .assesshelper import AssesmentHelper
from .models.language_models import LanguageModelManager
from .models.subject_models import SubjectModelManager
from .models.exam_models import ExamModelManager, Exam, LstSubjectExamModel
from .models.pattern_models import PaperPatternModelManager
# from .models.question_models import QuestionModelManager
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin


class CommonView(LoginRequiredMixin, View):
    
    template_name = "assessment/assessmentpage.html"
    def get(self, request, *args, **kwargs):
        exam_query = LstSubjectExamModel.objects.all().values_list('examid', flat=True).distinct()
        exam_query = json.dumps(list(exam_query))
        context = {}
        context['examids_lst'] = exam_query
        return render(self.request, self.template_name, context=context)


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
        # print("type of langiage id >>>>>>>>>>>>>. ", langId, type(langId))
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
            result, result_to_save = self.ash.exam_call(languageid, subjectid)
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

            #language api call and save in db
            result_lang = self.ash.language_call()
            if result_lang['status'] == 200:
                LanguageModelManager.save_language_data(self, result_lang['lang_result'])

                #subject api call and save in db
                for lids in languageIds:
                    result_subj = self.ash.subject_call(lids)
                    if result_subj['status'] == 200:
                        print(type(result_subj['subj_result']))
                        SubjectModelManager.save_subject_data(self, result_subj['subj_result'], lids)

                ##Exam api call and save in db
                for nlids in languageIds:
                    for sids in subjectIds:
                        result_ui, result_exam = self.ash.exam_call(nlids, sids, examIds)
                        if result_exam['status'] == 200:
                            ExamModelManager.save_exam_data(self, result_exam['exam_result'], nlids, sids)
            lst_of_pattern = []
            for eids in examIds:
                result_pattern = self.ash.pattern_call(eids)
                lst_of_pattern.append(result_pattern['exam_pattern'])
                PaperPatternModelManager.save_pattern_data(self, result_pattern['exam_pattern'], eids)

            #question api call
            quesPatternDetails = self.ash.question_details(languageIds, lst_of_pattern)

            context = {}
            context['message'] = "successfully saved"
            # print(context)
        return JsonResponse(context, safe=False)


