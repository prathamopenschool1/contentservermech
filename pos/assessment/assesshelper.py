import os
import json
import requests
import traceback
from pprint import pprint
from clint.textui import progress
from channels.file_downloader import Downloader

downloads = Downloader() 



class AssesmentHelper(object):

    language_data_to_save = ""
    subject_to_save = []
    languageId = ""
    exam_results = []
    unique_exam_data = []

    headers = {
        'cache-control': "no-cache",
        'content-type': "application/json",
        "Accept": "application/json"
    }

    # unique__data

    def __init__(self):
        pass

    def language_call(self):

        try:
            result = {}
            lang_url = "http://www.prathamassessment.org:8085/api/language/GetLanguage"
            lang_response = requests.get(lang_url)
            lang_result = json.loads(lang_response.content.decode('utf-8'))
            result['status'] = 200
            result['lang_result'] = lang_result
            AssesmentHelper.language_data_to_save = lang_result
            # LanguageModelManager.save_language_data(self, lang_to_save_result)
            # SubjectModelManager.save_subject_data(self, subj_to_save_result)
            return result
        except Exception as e:
            traceback.print_exc()
            print("exception is ", e)
            return -1


    def subject_call(self, langId):
        try:
            AssesmentHelper.languageId = langId
            result = {}
            subj_url = 'http://www.prathamassessment.org:8085/api/subject/GetSubjectv2?languageid={}'.format(langId)
            subj_response = requests.get(subj_url)
            subj_result = json.loads(subj_response.content.decode('utf-8'))
            # if isinstance(subj_result, list):
            #     subj_result.append({'languageid': langId})
            # print(subj_result, ">>>>>>>>>>>>>>>>>>>>>", type(subj_result))
            result['status'] = 200
            result['subj_result'] = subj_result
            AssesmentHelper.subject_to_save.append(subj_result)
            return result
        except Exception as e:
            traceback.print_exc()
            print("exception is ", e)
            return -1


    def exam_call(self, langId, subjId, examIds=None):
        try:
            result_to_save = {}
            result = {}
            exam_dicts = {}
            lst_exam_result = []
            lstsubjectexamLst = []
            exam_url = 'http://www.prathamassessment.org:8085/api/subjectexam/GetExamV2?subjectid={}&languageid={}'.format(subjId, langId)
            exam_response = requests.get(exam_url)
            exam_result = json.loads(exam_response.content.decode('utf-8'))
            print("ex ids ", examIds)
            if examIds is not None:
                for eids in examIds:
                    for data in exam_result:
                        exam_dicts['subjectid'] = data['subjectid']
                        exam_dicts['subjectname'] = data['subjectname']
                    for elem in exam_result[0]['lstsubjectexam']:
                        if elem['examid'] == int(eids):
                            lstsubjectexamLst.append(elem)
                
            exam_dicts['lstsubjectexam'] = lstsubjectexamLst
            lst_exam_result.append(exam_dicts)
            result['status'] = 200
            result['exam_result'] = exam_result
            result_to_save['status'] = 200
            result_to_save['exam_result'] = lst_exam_result
            AssesmentHelper.exam_results.append(exam_result)
            return result, result_to_save
        except Exception as e:
            traceback.print_exc()
            print("exception is ", e)
            return -1

    
    def pattern_call(self, examId):
        try:
            result = {}
            exam_pattern = []
            # for ids in examId:
            pattern_url = 'http://www.prathamassessment.org:8085/api/exampattern/GetExamPattern'
            pattern_response = requests.get(pattern_url, params={"examid": examId})
            pattern_result = json.loads(pattern_response.content.decode('utf-8'))
            # exam_pattern.append(pattern_result)
            result['status'] = 200
            result['exam_pattern'] = pattern_result
            return result
        except Exception as e:
            traceback.print_exc()
            print("exception is ", e)
            return -1


    def question_details(self, languageLst, examLst):
        try:
            result = {}
            questions_lst = []
            i=1
            print("my exam list ", examLst)
            for lid in languageLst:
                for sid in examLst:
                    for tid in sid['lstpatterndetail']:
                        quest_urls = 'http://www.prathamassessment.org:8085/api/question/GetQuestion'
                        quest_response = requests.get(quest_urls, params={'languageid': lid, 'subjectid': sid['subjectid'], 'topicid': tid['topicid']})
                        quest_result = json.loads(quest_response.content.decode('utf-8'))
                        if len(quest_result) > 0:
                            download_response = downloads.download_assesment_data('Assessment', quest_result)
                            # if download_response['status'] == 200:
                            # questions_lst.append(quest_result)
                        print(quest_result)
                        print("this is quest result ?????????????????????????...................", i)
                        print()
                        i=i+1

            return questions_lst
        except Exception as e:
            traceback.print_exc()
            return '-1'


    def fetch_accurate(self, languageIds=None, subjectIds=None, examIds=None):
        lst_sids = []
        lst_eids = []
        try:
            if languageIds is not None and subjectIds is not None and examIds is not None:
                
                # language dict list
                lst_lids = [ldata for lids in languageIds for ldata in AssesmentHelper.language_data_to_save if ldata['languageid'] == int(lids)]
                
                # subject dict list
                for sids in subjectIds:
                    for subj_data in AssesmentHelper.subject_to_save:
                        for selems in subj_data:
                            if not selems in lst_sids:
                                if selems['subjectid'] == int(sids):
                                    lst_sids.append(selems)

                # exam dict list
                for eids in examIds:
                    for elem in AssesmentHelper.exam_results:
                        for vals in elem[0]['lstsubjectexam']:
                            if not elem[0] in lst_eids:
                                if vals['examid'] == int(eids):
                                    lst_eids.append(elem[0])

                # print("lang >>>> ", lst_lids)
                # print("subj >>>> ", lst_sids)
                # print("exms >>>> ", lst_eids)
                # AssesmentHelper.unique_exam_data = lst_eids
                return lst_lids, lst_sids, lst_eids, AssesmentHelper.languageId

        except Exception as e:
            traceback.print_exc()
            return '-1'
                        



    