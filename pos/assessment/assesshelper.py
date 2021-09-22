import os
import json
import requests
import traceback
from pprint import pprint



class AssesmentHelper(object):

    language_data_to_save = ""
    subject_to_save = ""

    def language_call(self):

        try:
            result = {}
            lang_url = "http://www.prathamassessment.org:8085/api/language/GetLanguage"
            lang_response = requests.get(lang_url)
            lang_result = json.loads(lang_response.content.decode('utf-8'))
            result['status'] = 200
            result['lang_result'] = lang_result
            self.language_data_to_save = lang_result
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
            self.subject_to_save = subj_result
            return result
        except Exception as e:
            traceback.print_exc()
            print("exception is ", e)
            return -1


    def exam_call(self, langId, subjId):
        try:
            result = {}
            exam_url = 'http://www.prathamassessment.org:8085/api/subjectexam/GetExamV2?subjectid={}&languageid={}'.format(subjId, langId)
            exam_response = requests.get(exam_url)
            exam_result = json.loads(exam_response.content.decode('utf-8'))
            result['status'] = 200
            result['exam_result'] = exam_result
            return result
        except Exception as e:
            traceback.print_exc()
            print("exception is ", e)
            return -1

    
    def pattern_call(self, examId):
        try:
            result = {}
            exam_pattern = []
            for ids in examId:
                pattern_url = 'http://www.prathamassessment.org:8085/api/exampattern/GetExamPattern'
                pattern_response = requests.get(pattern_url, params={"examid": ids})
                pattern_result = json.loads(pattern_response.content.decode('utf-8'))
                exam_pattern.append(pattern_result)
            result['status'] = 200
            result['exam_pattern'] = exam_pattern
            return result
        except Exception as e:
            traceback.print_exc()
            print("exception is ", e)
            return -1


    def question_details(self, languageLst, examLst):
        try:
            result = {}
            for lid in languageLst:
                for sid in examLst:
                    for tid in sid['lstpatterndetail']:
                        print("question ", lid, sid['subjectid'], sid['subjectname'], sid['examname'], sid['examid'], tid['topicid'], tid['topicname'])
                        quest_urls = 'http://www.prathamassessment.org:8085/api/question/GetQuestion'
                        quest_response = requests.get(quest_urls, params={'languageid': lid, 'subjectid': sid['subjectid'], 'topicid': tid['topicid']})
                        quest_result = json.loads(quest_response.content.decode('utf-8'))
                        print(quest_result)
                        print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
        except Exception as e:
            traceback.print_exc()
            return -1

    