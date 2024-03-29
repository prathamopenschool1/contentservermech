from importlib.resources import path
import os
import json
import requests
import platform
import logging
import traceback
from zipfile import ZipFile
from clint.textui import progress
from urllib.request import urlopen
from assessment.models.question_models import QuestionModel, LstQuestionChoiceModel

# This retrieves a Python logging instance (or creates it)
infoLogger = logging.getLogger("info_logger")
errorLogger = logging.getLogger("error_logger")

# os.system('cd static/')

class Downloader(object):

    store_files = None
    store_img = None
    content = None
    files_data = None
    zip_files = None
    video_files = None
    audio_files = None
    m4v_files = None
    mp4_files = None
    mp3_files = None
    wav_files = None
    pdf_files = None
    wrong_extension = None
    localUrl = ""
    v3gp_files = ""
    a3gpp_files = ""
    m4a_files = ""
    amr_files = ""
    local_photo_url = ""
    local_match_url = ""
    local_choice_url = ""
    

    current_dir = os.getcwd()
    # print('old current_dir', current_dir)
    new_current_dir = os.path.join(current_dir, 'static')
    # print('after join', new_current_dir)
    os.chdir(new_current_dir)
    new_current_dir = os.getcwd()
    # print("new dir is", new_current_dir)

    headers = {
        'cache-control': "no-cache",
        'content-type': "application/json",
        "Accept": "application/json"
    }

    def createDir_if_not(self, file_path):
        if not os.path.exists(file_path):
            os.makedirs(file_path)

    def createdir(self, AppName):
        self.store_files = os.path.join(self.new_current_dir, 'storage')
        # print('sf', store_files)
        self.createDir_if_not(self.store_files)

        self.store_files = os.path.join(self.store_files, AppName)
        print('sf', self.store_files)
        self.createDir_if_not(self.store_files)

        # images folder
        self.store_img = os.path.join(self.store_files, 'images')
        print('simg', self.store_img)
        self.createDir_if_not(self.store_img)

        # content (videos and zips)
        self.content = os.path.join(self.store_files, 'content')
        # print('content', content)
        self.createDir_if_not(self.content)

        self.zip_files = os.path.join(self.content, 'zips')
        # print('content', content)
        self.createDir_if_not(self.zip_files)

        self.audio_files = os.path.join(self.content, 'audios')
        # print('content', content)
        self.createDir_if_not(self.audio_files)

        self.mp3_files = os.path.join(self.audio_files, 'mp3')
        # print('content', content)
        self.createDir_if_not(self.mp3_files)

        self.wav_files = os.path.join(self.audio_files, 'wav')
        # print('content', content)
        self.createDir_if_not(self.wav_files)

        self.video_files = os.path.join(self.content, 'videos')
        # print('content', content)
        self.createDir_if_not(self.video_files)

        self.mp4_files = os.path.join(self.video_files, 'mp4')
        # print('content', content)
        self.createDir_if_not(self.mp4_files)

        self.m4v_files = os.path.join(self.video_files, 'm4v')
        # print('content', content)
        self.createDir_if_not(self.m4v_files)

        self.pdf_files = os.path.join(self.content, 'docs')
        # print('content', content)
        self.createDir_if_not(self.pdf_files)

        self.wrong_extension = os.path.join(self.content, 'wrong_extensions')
        # print('content', content)
        self.createDir_if_not(self.wrong_extension)

        self.v3gp_files = os.path.join(self.video_files, '3gp')
        self.createDir_if_not(self.v3gp_files)

        self.a3gpp_files = os.path.join(self.audio_files, '3gpp')
        self.createDir_if_not(self.a3gpp_files)

        self.m4a_files = os.path.join(self.audio_files, 'm4a')
        self.createDir_if_not(self.m4a_files)

        self.amr_files = os.path.join(self.audio_files, 'amr')
        self.createDir_if_not(self.amr_files)


    def download_files_with_qs(self, download_url, querystring, AppName):
        print("url is ", download_url)
        #infoLogger.info(" In download_files_with_qs")
        self.createdir(AppName)
        response = requests.get(download_url, params=querystring, headers=self.headers)
        # print(response)
        result = json.loads(response.content.decode('utf-8'))
        # print(result, type(result))

        for detail in result:
            for key, value in detail.items():
                if key == 'LstFileList':
                    self.files_data = value

        try:
            for data in self.files_data:
                file_url = data["FileUrl"]
                if data["FileType"] == "Thumbnail":
                    path_to_put = os.path.join(
                        self.store_img, str(os.path.basename(file_url)))
                elif data["FileType"] == "Content" and file_url.endswith('.mp4'):
                    path_to_put = os.path.join(
                        self.mp4_files, str(os.path.basename(file_url)))
                elif data["FileType"] == "Content" and file_url.endswith('.MP4'):
                    file_url = file_url.replace('.MP4', '.mp4')
                    path_to_put = os.path.join(
                        self.mp4_files, str(os.path.basename(file_url)))
                elif data["FileType"] == "Content" and file_url.endswith('.m4v'):
                    path_to_put = os.path.join(
                        self.m4v_files, str(os.path.basename(file_url)))
                elif data["FileType"] == "Content" and file_url.endswith('.mp3'):
                    path_to_put = os.path.join(
                        self.mp3_files, str(os.path.basename(file_url)))
                elif data["FileType"] == "Content" and file_url.endswith('.MP3'):
                    file_url = file_url.replace('.MP3', '.mp3')
                    path_to_put = os.path.join(
                        self.mp3_files, str(os.path.basename(file_url)))
                elif data["FileType"] == "Content" and file_url.endswith('.wav'):
                    path_to_put = os.path.join(
                        self.wav_files, str(os.path.basename(file_url)))
                elif data["FileType"] == "Content" and file_url.endswith('.zip'):
                     if "prodigi.openiscool.org/Repository" in file_url:
                        file_url1 = file_url.replace("prodigi.openiscool.org/Repository","prathamopenschool.org/CourseContent")
                        path_to_put = os.path.join(
                          self.zip_files, str(os.path.basename(file_url1)))
                     else :
                         path_to_put = os.path.join(
                          self.zip_files, str(os.path.basename(file_url)))     
                elif data["FileType"] == "Content" and file_url.endswith('.pdf' or '.doc'):
                    path_to_put = os.path.join(
                        self.pdf_files, str(os.path.basename(file_url)))
                elif data["FileType"] == "Content" and file_url.endswith('.png'):
                    path_to_put = os.path.join(
                        self.wrong_extension, str(os.path.basename(file_url)))
                elif data["FileType"] == "Content" and file_url.endswith('.mpeg'):
                    path_to_put = os.path.join(
                        self.wrong_extension, str(os.path.basename(file_url)))
                elif data["FileType"] == "Content" and file_url.endswith('.jpg'):
                    path_to_put = os.path.join(
                        self.wrong_extension, str(os.path.basename(file_url)))
                elif data["FileType"] == "Content" and file_url.endswith('.jpeg'):
                    path_to_put = os.path.join(
                        self.wrong_extension, str(os.path.basename(file_url)))
                try:
                    if file_url == '':
                        continue
                    elif "prathamopenschool.org" not in file_url:
                        continue
                    else:
                        self.localUrl = path_to_put
                        # print("local path is ", self.localUrl)
                        file_to_get = requests.get(
                            file_url, stream=True, timeout=10)
                        print(file_to_get.status_code, 'status code ', file_url)
                        if file_to_get.status_code != 200:
                            continue
                        else:
                            # print("path to put is ", path_to_put)
                            with open(path_to_put, "wb") as target:
                                total_length = int(file_to_get.headers.get('content-length'))
                                # print("total length is >>> ", total_length)
                                for chunk in progress.bar(file_to_get.iter_content(chunk_size=1024),
                                                            expected_size=(total_length/1024) + 1):
                                    if chunk:
                                        try:
                                            target.write(chunk)
                                            target.flush()
                                        except requests.exceptions.ConnectionError as dataflush_err:
                                            print("Exception occurd while flushing data ", str(dataflush_err))
                                            errorLogger.error("Exception occurd while flushing data" + str(dataflush_err))
                
                except requests.exceptions.ConnectionError as dwnld_files_with_qs_error1:
                    print(" no internet in download_files_with_qs ", dwnld_files_with_qs_error1)
                    errorLogger.error(" no internet in download_files_with_qs "+ str(dwnld_files_with_qs_error1))
                    #commented treturn false to continue downloading after internet is up again and added continue below
                    return False
                    # continue

        except requests.exceptions.ConnectionError as dwnld_files_with_qs_error2:
            print("in download_files_with_qs  ", dwnld_files_with_qs_error2)
            errorLogger.error("e_error in download_files_with_qs " + str(dwnld_files_with_qs_error2))
            return False

        # print("with qs local ", self.localUrl)
        # return localUrl


    # download("http://devposapi.prathamopenschool.org/Api/AppNodeDetailListByNode", {"id": "1"})


    def download_files_without_qs(self, download_url, AppName):
        #infoLogger.info(" In download_files_without_qs")
        self.createdir(AppName)
        response = requests.get(download_url, headers=self.headers)
        print(response)
        result = json.loads(response.content.decode('utf-8'))
        # print(result, type(result))

        try:
            for detail in result:
                file_url = detail['ThumbUrl']
                if file_url.endswith('.png'):
                    path_to_put = os.path.join(
                            self.store_img, str(os.path.basename(detail['ThumbUrl'])))
                    # print(path_to_put)
                    # print(detail, type(detail))
                file_to_get = requests.get(
                            file_url, stream=True, timeout=10)
                if file_to_get.status_code != 200:
                            continue
                else:
                    with open(path_to_put, "wb") as target:
                            total_length = int(
                                file_to_get.headers.get('content-length'))
                            for chunk in progress.bar(file_to_get.iter_content(chunk_size=1024),
                                                        expected_size=(total_length/1024) + 1):
                                if chunk:
                                    target.write(chunk)
                                    target.flush()
                            self.localUrl = path_to_put
            # return True
        except requests.exceptions.ConnectionError as dwnld_files_without_qs_error:
            print("in download_files_without_qs  ", dwnld_files_without_qs_error)
            errorLogger.error("e_error in download_files_without_qs " + str(dwnld_files_without_qs_error))
            return False
        
        # print("this is ", self.localUrl)

    

    def download_assesment_data(self, AppName, quest_result):

        photo_url = ""
        match_url = ""
        choice_url = ""

        try:
            self.createdir(AppName)
            for res in quest_result:
                photo_url = res['photourl']
                if photo_url != '':
                    fetched_url_val = self.common_extensions(photo_url, photo=1)
                qobj, qcreated = QuestionModel.objects.get_or_create(
                    languageid      = res['languageid'],
                    qid             = res['qid'],
                    subjectid       = res['subjectid'],
                    topicid         = res['topicid'],
                    lessonid        = res['lessonid'],
                    qtid            = res['qtid'],
                    qname           = res['qname'],
                    answer          = res['answer'],
                    photourl        = res['photourl'],
                    ansdesc         = res['ansdesc'],
                    qlevel          = res['qlevel'],
                    hint            = res['hint'],
                    addedby         = res['addedby'],
                    addedtime       = res['addedtime'],
                    updatedby       = res['updatedby'],
                    updatedtime     = res['updatedtime'],
                    IsParaQuestion  = res['IsParaQuestion'],
                    RefParaID       = res['RefParaID'],
                    isdeleted       = res['isdeleted'],
                    AppVersion      = res['AppVersion'],
                    localPhotoUrl   = self.local_photo_url if photo_url != "" else ""
                )
                if len(res['lstquestionchoice']) > 0:
                    for lst in res['lstquestionchoice']:
                        match_url = lst['matchingurl']
                        choice_url = lst['choiceurl']
                        if match_url != "":
                            fetched_url_val = self.common_extensions(match_url, match=1)
                        if choice_url != "":
                            fetched_url_val = self.common_extensions(choice_url, choice=1)
                        lobj, lcreated = LstQuestionChoiceModel.objects.get_or_create(
                            lstquestionchoice   = qobj,
                            qid = lst['qid'],
                            qcid    = lst['qcid'],
                            matchingname    = lst['matchingname'],
                            choicename  = lst['choicename'],
                            correct = lst['correct'],
                            matchingurl = lst['matchingurl'],
                            choiceurl   = lst['choiceurl'],
                            AppVersionChoice    = lst['AppVersionChoice'],
                            localMatchUrl   = self.local_match_url if match_url != "" else "",
                            localChoiceUrl  = self.local_choice_url if choice_url != "" else ""
                        )

                
        except requests.exceptions.ConnectionError as dwnld_files_asess_error2:
            # print("traceback error 1 here >>>> ", traceback.print_exc())
            # print("in download_files_with_asessment  ", dwnld_files_asess_error2)
            errorLogger.error("in download_files_with_asessment  " + str(dwnld_files_asess_error2))


    def common_extensions(self, extension_url, match=0, photo=0, choice=0):
        
        download_result = {}
        path_to_put_asses = ""
        if extension_url.endswith('.png'):
            path_to_put_asses = os.path.join(self.store_img, os.path.basename(extension_url))
            # print("my image path >>> ", path_to_put_asses)
        elif extension_url.endswith('.PNG'):
            extension_url = extension_url.replace('.PNG', '.png')
            path_to_put_asses = os.path.join(self.store_img, os.path.basename(extension_url))
            # print("my image path >>> ", path_to_put_asses)
        elif extension_url.endswith('.JPG'):
            extension_url = extension_url.replace('.JPG', '.jpg')
            path_to_put_asses = os.path.join(self.store_img, os.path.basename(extension_url))
            # print("my image path >>> ", path_to_put_asses)
        elif extension_url.endswith('.jpg'):
            path_to_put_asses = os.path.join(self.store_img, os.path.basename(extension_url))
            # print("my image path >>> ", path_to_put_asses)
        elif extension_url.endswith('.jpeg'):
            path_to_put_asses = os.path.join(self.store_img, os.path.basename(extension_url))
            # print("my image path >>> ", path_to_put_asses)
        elif extension_url.endswith('.JPEG'):
            extension_url = extension_url.replace('.JPEG', '.jpeg')
            path_to_put_asses = os.path.join(self.store_img, os.path.basename(extension_url))
            # print("my image path >>> ", path_to_put_asses)
        #videos
        elif extension_url.endswith('.MP4'):
            extension_url = extension_url.replace('.MP4', '.mp4')
            path_to_put_asses = os.path.join(self.mp4_files, os.path.basename(extension_url))
            # print("my videos path >>> ", path_to_put_asses)
        elif extension_url.endswith('.mp4'):
            path_to_put_asses = os.path.join(self.mp4_files, os.path.basename(extension_url))
            # print("my videos path >>> ", path_to_put_asses)
        elif extension_url.endswith('.3gp'):
            path_to_put_asses = os.path.join(self.v3gp_files, os.path.basename(extension_url))
            # print("my videos path >>> ", path_to_put_asses)
        #audios
        elif extension_url.endswith('.mp3'):
            path_to_put_asses = os.path.join(self.mp3_files, os.path.basename(extension_url))
            # print("my audios path >>> ", path_to_put_asses)
        elif extension_url.endswith('.MP3'):
            extension_url = extension_url.replace('.MP3', '.mp3')
            path_to_put_asses = os.path.join(self.mp3_files, os.path.basename(extension_url))
            # print("my audios path >>> ", path_to_put_asses)
        elif extension_url.endswith('.3gpp'):
            path_to_put_asses = os.path.join(self.a3gpp_files, os.path.basename(extension_url))
            # print("my audios path >>> ", path_to_put_asses)
        elif extension_url.endswith('.m4a'):
            path_to_put_asses = os.path.join(self.m4a_files, os.path.basename(extension_url))
            # print("my audios path >>> ", path_to_put_asses)
        elif extension_url.endswith('.amr'):
            path_to_put_asses = os.path.join(self.amr_files, os.path.basename(extension_url))
            # print("my audios path >>> ", path_to_put_asses)


        try:
            self.localUrl = path_to_put_asses
            if photo == 1 and self.localUrl != '':
                self.local_photo_url = self.localUrl
                self.local_photo_url = self.local_photo_url.split('static')[1]
                self.local_photo_url = 'http://192.168.4.1:8000/static'+self.local_photo_url
            if match == 1 and self.localUrl != '':
                self.local_match_url = self.localUrl
                self.local_match_url = self.local_match_url.split('static')[1]
                self.local_match_url = 'http://192.168.4.1:8000/static'+self.local_match_url
            if choice == 1 and self.localUrl != '':
                self.local_choice_url = self.localUrl
                self.local_choice_url = self.local_choice_url.split('static')[1]
                self.local_choice_url = 'http://192.168.4.1:8000/static'+self.local_choice_url

            if self.localUrl != '':
                file_to_get = requests.get(extension_url, stream=True, timeout=30)
                # print('status code extension url>>>>> ', extension_url)
                if file_to_get.status_code == 200:
                    with open(path_to_put_asses, "wb") as target:
                        total_length = int(file_to_get.headers.get('content-length'))
                        for chunk in progress.bar(file_to_get.iter_content(chunk_size=1024), expected_size=(total_length/1024) + 1):
                            if chunk:
                                try:
                                    target.write(chunk)
                                    target.flush()
                                except requests.exceptions.ConnectionError as dataflush_err:
                                    # print("Exception occurd while flushing data ", str(dataflush_err))
                                    errorLogger.error("Exception occurd while flushing data" + str(dataflush_err))

                        download_result['status'] = 200
                        return download_result
        except requests.exceptions.ConnectionError as dwnld_files_asess_error2:
            # print("traceback error 2 here >>>> ",traceback.print_exc())
            # print("in download_files_with_asessment  ", dwnld_files_asess_error2)
            errorLogger.error("e_error in download_files_with_asessment " + str(dwnld_files_asess_error2))
            download_result['status'] = 505 
            return download_result
        








# download = Downloader()
# download.download_files_with_qs("http://devposapi.prathamopenschool.org/Api/AppNodeDetailListByNode",
#                         {"id": "ee486417-0216-47ec-a493-56622a800503"})
# download.download_files_without_qs("http://devposapi.prathamopenschool.org/api/AppList")
