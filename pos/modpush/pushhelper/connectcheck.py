import os
import json
import shutil
import logging
import requests
import traceback
import datetime
from pathlib import Path
from urllib.request import urlopen
from common_helper.helper import CommonHelpers


infoLogger = logging.getLogger("info_logger")
errorLogger = logging.getLogger("error_logger")


class PushHelper(object):

    homePath = str(Path.home())
    deskDir = os.path.join(homePath, 'DesktopBackup')

    #usage post api
    post_url = "http://devprodigi.openiscool.org/api/RPIAppZipPush/PushFiles"

    #db post api
    db_post_url = "http://devprodigi.openiscool.org/api/RPIAppDB/PushFiles"

    #desktop post api
    desktop_post_url = "http://rpi.prathamskills.org/api/KolibriSession/Post"


    headers = {
        'cache-control': "no-cache",
        'content-type': "application/json",
        'Accept': 'application/json'
    }

    #To Check internet is avialble or not
    def connect(self, host="https://www.google.com/"):
        try:
            urlopen(host)
            return True
        except:
            return False

    # usagedata
    def push_usageData(self):
        
        pageNo = 1
        serial_line = ''
        status_quo = {}
        result_set = {}

        usagedata_url = "http://192.168.4.1:8000/api/usagedata/"
        response = requests.get(usagedata_url)
        lstscore = json.loads(response.content.decode('utf-8'))

        # pi id data to be collected
        os.system('cat /proc/cpuinfo > serial_data.txt')
        serial_file = open('serial_data.txt', "r+")
        for line in serial_file:
            if line.startswith('Serial'):
                serial_line = line

        lstscore['serial_id'] = serial_line

        if lstscore['count'] == 0:
            infoLogger.info("no data")
            status_quo['status'] = 403
            status_quo['msg'] = 'Data Not Found'
            return status_quo

        else:
            while True:
                fetch_url = "http://192.168.4.1:8000/api/usagedata/?page={}&page_size=15".format(pageNo)
                usage_response = requests.get(fetch_url)
                data = json.loads(usage_response.content.decode('utf-8'))

                if data['count'] == 0 and data['next'] is None:
                    result_set['status'] = 400
                    return result_set
                elif data['count'] != 0 and data['next'] is None:
                    result_set = self.usageFile(data)
                    return result_set
                else:
                    result_set = self.usageFile(data)
                    # return result_set
                    if data['count'] == 0 and data['next'] is None:
                        return result_set
                    else:
                        result_set = self.usageFile(data)

                pageNo =  pageNo + 1
    

    def usageFile(self, data):
        result_set = {}
        try:
            for i in range(len(data['results'])):                    
                actualfileName = data['results'][i]["uploaded_file"]
                actualfileName = actualfileName.replace("http://192.168.4.1:8000", os.path.join(self.homePath, "contentservermech/pos"))
                lastndexofFwdSlsh = actualfileName.rfind('/')                    
                filenamestr = actualfileName[lastndexofFwdSlsh + 1:len(actualfileName)]
                indexofDotzip = filenamestr.index(".zip")
                filenamestr = filenamestr[0:indexofDotzip]
                if os.path.isfile(actualfileName):
                    datasws = {filenamestr: open(actualfileName, 'rb')}
                    response_post = requests.post(self.post_url,files = datasws)           
                    infoLogger.info("response_post sws "+ str(response_post.status_code))    
                    if response_post.status_code == 200:
                        os.remove(actualfileName)
                        result_set["status"] = 202
                else:
                    infoLogger.info("Error, File "+ actualfileName +" not exists")
                    result_set['status'] = 400
            
            # result_set['status'] = 200
            return result_set

        except Exception as e1:
            errorLogger.error("Error push_usageData is: " + str(e1))
            result_set["status"] = 404
            result_set['msg'] = e1
            return result_set


    # dbpush helper function
    def push_dbPushData(self):

        pageNo = 1
        status_quo = {}
        result_set = {}

        dbpush_url = "http://192.168.4.1:8000/api/dbpushdata/"
        response = requests.get(dbpush_url)
        dbpushdata = json.loads(response.content.decode('utf-8'))

        if dbpushdata['count'] == 0:
            infoLogger.info("no data")
            status_quo['status'] = 403
            status_quo['msg'] = 'Data Not Found'
            return status_quo

        else:
            while True:
                fetch_url = "http://192.168.4.1:8000/api/dbpushdata/?page={}&page_size=15".format(pageNo)
                usage_response = requests.get(fetch_url)
                data = json.loads(usage_response.content.decode('utf-8'))

                if data['count'] == 0 and data['next'] is None:
                    result_set['status'] = 400
                    return result_set
                elif data['count'] != 0 and data['next'] is None:
                    result_set = self.usageFile(data)
                    return result_set
                else:
                    result_set = self.usageFile(data)
                    # return result_set
                    if data['count'] == 0 and data['next'] is None:
                        return result_set
                    else:
                        result_set = self.usageFile(data)

                pageNo =  pageNo + 1


    #descktop data function
    def desktop_data_to_server(self):
        desktop_resultlist = []
        pageNo = 1
        status_quo = {}
        result_set = {}

        desktop_url = 'http://192.168.4.1:8000/api/desktopdata/'
        appList_url = 'http://192.168.4.1:8000/api/channel/AppList/'

        dresponse = requests.get(desktop_url)
        aresponse = requests.get(appList_url)

        dresult = json.loads(dresponse.content.decode('utf-8'))
        aresult = json.loads(aresponse.content.decode('utf-8'))

        if dresult['count'] == 0 and aresult['count'] == 0:
            infoLogger.info("No Data Found in both Applist and DeskTop w/o loop")
            status_quo['status'] = 403
            status_quo['msg'] = 'Data Not Found'
            return status_quo
        elif dresult['count'] == 0:
            infoLogger.info("No Data Found in both Applist or DeskTop")
            status_quo['status'] = 403
            status_quo['msg'] = 'Data Not Found'
            # print("status quo ", status_quo)
            return status_quo
        else:
            while True:
                # get api
                desktop_url = "http://192.168.4.1:8000/api/desktopdata/?page={}&page_size=15".format(pageNo)
                appList_url = "http://192.168.4.1:8000/api/channel/AppList/"

                # desktop data url
                desktop_response = requests.get(desktop_url, headers=self.headers)
                desktop_result = json.loads(desktop_response.content.decode('utf-8'))

                # app list url
                appList_response = requests.get(appList_url, headers=self.headers)
                appList_result = json.loads(appList_response.content.decode('utf-8'))

                if desktop_response.status_code == 404 and appList_response.status_code == 404:
                    infoLogger.info("No Data Found in both Applist and DeskTop")
                    status_quo['status'] = 404
                    status_quo['msg'] = 'Data Not Found'
                    return status_quo
                elif desktop_response.status_code == 404:
                    infoLogger.info("No Data Found in DeskTop")
                    desktop_data_to_post_list = {
                            "desktop_resultlist": desktop_resultlist,                        
                    }
                    desktop_data_to_post_list['status'] = 203
                    # print("new desktop ", desktop_data_to_post_list)
                    return desktop_data_to_post_list
                else:
                    if desktop_result['count'] == 0 and desktop_result['next'] is None:
                        result_set['status'] = 400
                        return result_set
                    elif desktop_result['count'] != 0 and desktop_result['next'] is None:
                        result_set = self.desktopFile(desktop_result, appList_result, desktop_resultlist)
                        return result_set
                    else:
                        result_set = self.desktopFile(desktop_result, appList_result, desktop_resultlist)
                        if desktop_result['count'] == 0 and desktop_result['next'] is None:
                            return result_set
                        else:
                            result_set = self.desktopFile(desktop_result, appList_result, desktop_resultlist)

                pageNo =  pageNo + 1


    def desktopFile(self, desktop_result, appList_result, desktop_resultlist):
        result_set = {}
        try:
            desktop_data_to_post = {
                "desktop_result": desktop_result,
                "appList_result": appList_result,
            }
            requests.post(
                self.desktop_post_url,
                headers=self.headers,
                data=json.dumps(desktop_data_to_post),
            )
            
            #appending desktop_result to desktop_resultlist when next is none in API result
            desktop_resultlist.append(desktop_result)

            result_set['status'] = 202
            return result_set

        except Exception as e1:
            # return False
            errorLogger.error("Error in desktop_data_to_server : " + str(e1))
            # return render(request, 'push/data_to_push.html')
            result_set["status"] = 404
            result_set['msg'] = e1
            return result_set


    def create_usage_directory(self):
        homeDir = os.path.join(self.homePath, "generate/Backup")
        usageDir = os.path.join(homeDir, "usageData")
        infoLogger.info("usageDir : " + usageDir)
        if not os.path.exists(usageDir):
            os.makedirs(usageDir)

        print("usageDir is from create_dir ", homeDir, usageDir)
        return usageDir

    # for DB Push Data
    def create_dbpush_directory(self):
        homeDir = os.path.join(self.homePath, "generate/Backup")
        dbpushDir = os.path.join(homeDir, "dbPushData")
        infoLogger.info("dbpushDir : " + dbpushDir)
        if not os.path.exists(dbpushDir):
            os.makedirs(dbpushDir)

        print("dbpushDir is from create_dir ", homeDir, dbpushDir)                    
        return dbpushDir


    def create_desktop_directory(self):
        homeDir = os.path.join(self.homePath, "generate/Backup")
        desktopDir = os.path.join(homeDir, "desktopData")
        infoLogger.info("desktopDir : " + desktopDir)
        if not os.path.exists(desktopDir):
            os.makedirs(desktopDir)

        print("deskDir is from create_dir ", homeDir, desktopDir)
        return desktopDir



    def backup(self):
        chp = CommonHelpers()
        randstr = chp.get_secret_string(6)
        pageNo = 1

        status_quo = {}
        result_set = {}

        destDir = os.path.join(self.create_usage_directory(), randstr + str(datetime.datetime.now()))
        srcDir = os.path.join(self.homePath, 'contentservermech/pos/media/usage')
        if os.listdir(srcDir):
            shutil.copytree(srcDir, destDir, symlinks = True)

        # added for DB Push
        destDbPushDir = os.path.join(self.create_dbpush_directory(), randstr + str(datetime.datetime.now()))
        srcDbPushDir = os.path.join(self.homePath, 'contentservermech/pos/media/dbpushdata')
        if os.listdir(srcDbPushDir):    
            shutil.copytree(srcDbPushDir, destDbPushDir, symlinks = True)


        desktop_url = 'http://192.168.4.1:8000/api/desktopdata/'
        appList_url = 'http://192.168.4.1:8000/api/channel/AppList/'

        dresponse = requests.get(desktop_url)
        aresponse = requests.get(appList_url)

        dresult = json.loads(dresponse.content.decode('utf-8'))
        aresult = json.loads(aresponse.content.decode('utf-8'))

        if dresult['count'] == 0 and aresult['count'] == 0:
            infoLogger.info("No Data Found in both Applist and DeskTop w/o loop")
            status_quo['status'] = 403
            status_quo['msg'] = 'Data Not Found'
            return status_quo
        elif dresult['count'] == 0:
            infoLogger.info("No Data Found in both Applist or DeskTop")
            status_quo['status'] = 403
            status_quo['msg'] = 'Data Not Found'
            # print("status quo ", status_quo)
            return status_quo
        else:
            while True:
                # get api
                desktop_url = "http://192.168.4.1:8000/api/desktopdata/?page={}&page_size=15".format(pageNo)
                appList_url = "http://192.168.4.1:8000/api/channel/AppList/"

                # desktop data url
                desktop_response = requests.get(desktop_url, headers=self.headers)
                desktop_result = json.loads(desktop_response.content.decode('utf-8'))

                # app list url
                appList_response = requests.get(appList_url, headers=self.headers)
                appList_result = json.loads(appList_response.content.decode('utf-8'))

                if desktop_response.status_code == 404 and appList_response.status_code == 404:
                    infoLogger.info("No Data Found in both Applist and DeskTop")
                    status_quo['status'] = 404
                    status_quo['msg'] = 'Data Not Found'
                    return status_quo
                else:
                    if desktop_result['count'] != 0 and desktop_result['next'] is None:
                        result_set = self.backupFile(desktop_result, appList_result)
                        return result_set
                    else:
                        result_set = self.backupFile(desktop_result, appList_result)
                        # if desktop_result['count'] == 0 and desktop_result['next'] is None:
                        #     return result_set
                        # else:
                        #     result_set = self.backupFile(desktop_result, appList_result)

                pageNo =  pageNo + 1


    def backupFile(self, desktop_result, appList_result):
        chp = CommonHelpers()
        randstr = chp.get_secret_string(6)

        result_set = {}
        try:
            desktop_data_to_post = {
                "desktop_result": desktop_result,
                "appList_result": appList_result,
            }
            try:
                with open(os.path.join(self.create_desktop_directory(),
                                    randstr + str(datetime.datetime.now()) + '.json'),
                        "w") as outfile:
                    json.dump(desktop_data_to_post, outfile, indent=4, sort_keys=True)
                    result_set['status'] = 202
                    return result_set
            except Exception as bkp_error_next:
                print("bkp error in desktop_data_to_post else part is ", bkp_error_next)
                errorLogger.error("bkp error in desktop_data_to_post else part is: " + str(bkp_error_next))
                result_set['status'] = 402
                result_set['msg'] = bkp_error_next
                return result_set

        except Exception as e1:
            errorLogger.error("Error in desktop_data_to_server : " + str(e1))
            result_set["status"] = 404
            result_set['msg'] = e1
            return result_set

    #new method added to delete zip files pushed from tab after pushing to server
    def deleteUsageZipFiles(self):
        dir = os.path.join(self.homePath, 'contentservermech/pos/media/usage')
        for f in os.listdir(dir):
            os.remove(os.path.join(dir,f))


    #new method added to delete db zip files pushed from tab after pushing to server
    def deleteDbPushZipFiles(self):
        dir = os.path.join(self.homePath, 'contentservermech/pos/media/dbpushdata')
        for f in os.listdir(dir):
            os.remove(os.path.join(dir,f))








    


