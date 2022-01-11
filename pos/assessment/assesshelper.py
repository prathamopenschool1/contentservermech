import os
import json
import requests
import traceback
from pprint import pprint
from clint.textui import progress
from channels.file_downloader import Downloader

downloads = Downloader() 



class AssesmentHelper(object):

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
            return result
        except Exception as e:
            traceback.print_exc()
            print("exception is ", e)
            return -1


    def subject_call(self, langId):
        try:
            result = {}
            subj_url = 'http://www.prathamassessment.org:8085/api/subject/GetSubjectv2?languageid={}'.format(langId)
            subj_response = requests.get(subj_url)
            subj_result = json.loads(subj_response.content.decode('utf-8'))
            result['status'] = 200
            result['subj_result'] = subj_result
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
            return result, result_to_save
        except Exception as e:
            traceback.print_exc()
            print("exception is ", e)
            return -1

    
    def pattern_call(self, examId):
        try:
            result = {}
            exam_pattern = []
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
            # questions_lst = []

            for lid in languageLst:
                for sid in examLst:
                    for tid in sid['lstpatterndetail']:
                        quest_urls = 'http://www.prathamassessment.org:8085/api/question/GetQuestion'
                        quest_response = requests.get(quest_urls, params={'languageid': lid, 'subjectid': sid['subjectid'], 'topicid': tid['topicid']})
                        quest_result = json.loads(quest_response.content.decode('utf-8'))
                        if len(quest_result) > 0:
                            download_response = downloads.download_assesment_data('Assessment', quest_result)

            result['status'] = 200
                    
            return result
        except Exception as e:
            # traceback.print_exc()
            return '-1'                        



    