import os,shutil
import json
import string
import random
import platform
import datetime
import requests
import time
import traceback
import logging
from pathlib import Path
from django.contrib import messages
# imported new model DbPushData for DB Push data API
from core.models import UsageData, DeskTopData,DbPushData
from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
from django.contrib.sessions.models import Session
from django.template import Template, Context
from django.views.generic import TemplateView
from urllib.request import urlopen

# This retrieves a Python logging instance (or creates it)
infoLogger = logging.getLogger("info_logger")
errorLogger = logging.getLogger("error_logger")

system_os = platform.system()
#print(system_os)
#infoLogger.info("system_os in push module: " + system_os)
#print(type(system_os))
#infoLogger.info("type of system_os in push module: " + type(system_os).__name__)



headers = {
    'cache-control': "no-cache",
    'content-type': "application/json",
    'Accept': 'application/json'
}
#To Check internet is avialble or not
def connect(host='http://google.com'):
    try:
        urlopen(host)
        return True
    except:
        return False


def push_data(request):
    return render(request, 'push/data_to_push.html')


def create_usage_directory():
    # global homeDir
    #print("usgd")
    if system_os == 'Windows':
        print("usgdata")
        infoLogger.info("system_os: " + system_os)
        homeDir = str(Path.home())
        homeDir = os.path.join(homeDir, r"generate\Backup")
        usageDir = os.path.join(homeDir, r"usageData")
        print(usageDir)
        if not os.path.exists(usageDir):
            os.makedirs(usageDir)
        else:
            pass
    else:
        print("linux")
        infoLogger.info("system_os: " + system_os)
        homeDir = str(Path.home())
        homeDir = os.path.join(homeDir, "generate/Backup")
        usageDir = os.path.join(homeDir, "usageData")
        if not os.path.exists(usageDir):
            os.makedirs(usageDir)
        else:
            pass

    # print("homeDir is from create_dir ", homeDir)
    return usageDir

# for DB Push Data
def create_dbpush_directory():
    
    if system_os == 'Windows':
        infoLogger.info("system_os: " + system_os)
        homeDir = str(Path.home())
        homeDir = os.path.join(homeDir, r"generate\Backup")
        dbpushDir = os.path.join(homeDir, r"dbPushData")
        infoLogger.info("dbpushDir : " + dbpushDir)
        print(dbpushDir)
        if not os.path.exists(dbpushDir):
            os.makedirs(dbpushDir)
        else:
            pass
    else:
        print("linux")
        infoLogger.info("system_os: " + system_os)
        homeDir = str(Path.home())
        homeDir = os.path.join(homeDir, "generate/Backup")
        dbpushDir = os.path.join(homeDir, "dbPushData")
        infoLogger.info("dbpushDir : " + dbpushDir)
        if not os.path.exists(dbpushDir):
            os.makedirs(dbpushDir)
        else:
            pass

       
    return dbpushDir


def create_desktop_directory():
    # global homeDir
    if system_os == 'Windows':
        try:
            print(system_os, "deskt")
            homeDir = str(Path.home())
            homeDir = os.path.join(homeDir, r"generate\Backup")
            desktopDir = os.path.join(homeDir, r"desktopData")
            print(desktopDir)
            if not os.path.exists(desktopDir):
                os.makedirs(desktopDir)
            else:
                pass
        except Exception as dir_err:
            print(dir_err)
            errorLogger.error("Error in create_desktop_directory is " + str(dir_err))
    else:
        homeDir = str(Path.home())
        homeDir = os.path.join(homeDir, "generate/Backup")
        desktopDir = os.path.join(homeDir, "desktopData")
        if not os.path.exists(desktopDir):
            os.makedirs(desktopDir)
        else:
            pass

    # print("homeDir is from create_dir ", homeDir)
    return desktopDir

# modified to check internet connection while adding code for DB Push
def push_usageData(request):
    infoLogger.info("In push_usageData")
    infoLogger.info("internet connection status" +  str(connect()))
    if connect():    
        pageNo = 1
        #n = 6
        serial_line = ''
        #randstr = ''.join(random.choice(
        #    string.ascii_uppercase + string.digits) for _ in range(n))

        while True:
            fetch_url = "http://192.168.1.16:8000/api/usagedata/?table_name=USAGEDATA&page=%s&page_size=15" % pageNo

            # post api
            #commeted out to use new API for zip upload 
            #post_url = "http://rpi.prathamskills.org/api/KolibriSession/Post"
            post_url = "http://devprodigi.openiscool.org/api/RPIAppZipPush/PushFiles"

            response = requests.get(fetch_url)

            lstscore = json.loads(response.content.decode('utf-8'))
            print("lstscore >>>>>>>>>>>>>>>>>>>>>>>>>>", lstscore['count'], lstscore)

            # pi id data to be collected
            os.system('cat /proc/cpuinfo > serial_data.txt')
            serial_file = open('serial_data.txt', "r+")
            for line in serial_file:
                if line.startswith('Serial'):
                    serial_line = line

            lstscore['serial_id'] = serial_line

            # checks the value of count
            if lstscore['count'] == 0 and lstscore['next'] is None:
                print("no data")
                infoLogger.info("no data")
                return render(request, 'push/data_to_push.html')
            elif lstscore['count'] != 0 and lstscore['next'] is None:
                try:
                    data = lstscore
                    for i in range(len(data['results'])):                    
                        actualfileName = data['results'][i]["uploaded_file"]
                        print("actualfileName >>>>>>>>>>>>>", actualfileName)
                        actualfileName = actualfileName.replace("http://192.168.1.16:8000", "/home/mark2/contentservermech/pos")
                        print("replaced filenae ===========================  ", actualfileName)
                        lastndexofFwdSlsh = actualfileName.rfind('/')                    
                        filenamestr = actualfileName[lastndexofFwdSlsh + 1:len(actualfileName)]
                        indexofDotzip = filenamestr.index(".zip")
                        filenamestr = filenamestr[0:indexofDotzip]
                        if os.path.isfile(actualfileName):
                            datasws = {filenamestr: open(actualfileName, 'rb')}
                            response_post = requests.post(post_url,files = datasws)
                            print("response_post",response_post.status_code)                       
                            infoLogger.info("response_post sws "+ str(response_post.status_code))    
                            if response_post.status_code == 200:
                                os.remove(actualfileName) 
                            
                        else:
                            print("Error, File "+ actualfileName +" not exists") 
                            infoLogger.info("Error, File "+ actualfileName +" not exists")                   
                    
                except Exception as bkp_error_next:
                    print("error push_usageData is ", bkp_error_next, traceback.print_exc())
                    errorLogger.error("Error push_usageData is: " + str(bkp_error_next))
                # To clear usage data after pushing usage data pos server
                clear_usage_data()    
                return render(request, 'push/data_to_push.html')
            else:
                
                try:
                    data = lstscore  # providing lstscore value to data variable
                    #print("length", len(data['results']))
                    #print("data " , data)
                    for i in range(len(data['results'])):                    
                        actualfileName = data['results'][i]["uploaded_file"]
                        print("only else file fname ", actualfileName)
                        actualfileName = actualfileName.replace("http://192.168.1.16:8000", "/home/mark2/contentservermech/pos")
                        lastndexofFwdSlsh = actualfileName.rfind('/')                    
                        filenamestr = actualfileName[lastndexofFwdSlsh + 1:len(actualfileName)]
                        indexofDotzip = filenamestr.index(".zip")
                        filenamestr = filenamestr[0:indexofDotzip]
                        if os.path.isfile(actualfileName):
                            datasws = {filenamestr: open(actualfileName, 'rb')}
                            response_post = requests.post(post_url,files = datasws)
                            print("response_post sws when lstscore['next'] is Not None",response_post.status_code)
                            infoLogger.info("response_post sws when lstscore['next'] is not None "+ str(response_post.status_code))    
                            
                            if response_post.status_code == 200:
                                os.remove(actualfileName) 
                            
                        else:
                            print("Error, File "+ actualfileName +" not exists when lstscore['next'] is not None") 
                            infoLogger.info("Error, File "+ actualfileName +" not exists when lstscore['next'] is not None")
                                       
                except Exception as e1:
                    print("Error in push_usageData when lstscore['next'] is not None: ", e1, traceback.print_exc())
                    errorLogger.error("Error in push_usageData when lstscore['next'] is not None: " + str(e1))
                    return False
            pageNo = pageNo+1        
        return render(request, 'push/data_to_push.html')
    else:    
        print("when no internetconnection")
        infoLogger.info("when no internetconnection")
        return render(request, 'push/no_internet.html')  

def backup(request):
    
    i = 1
    n = 6
    #serial_line = ''
    randstr = ''.join(random.choice(
        string.ascii_uppercase + string.digits) for _ in range(n))

    destDir = os.path.join(create_usage_directory(),
             randstr + str(datetime.datetime.now()))
    
    srcDir = '/home/mark2/contentservermech/pos/media/usage'
    if os.listdir(srcDir):    
        shutil.copytree(srcDir, destDir, symlinks = True)    

    # added for DB Push
    destDbPushDir = os.path.join(create_dbpush_directory(),
             randstr + str(datetime.datetime.now()))
    
    srcDbPushDir = '/home/mark2/contentservermech/pos/media/dbpushdata'
    if os.listdir(srcDbPushDir):    
        shutil.copytree(srcDbPushDir, destDbPushDir, symlinks = True)  

    while True:        

        # desktop data backup
        desktop_url = "http://192.168.1.16:8000/api/desktopdata/?page=%s&page_size=15" % i
        appList_url = "http://192.168.1.16:8000/api/channel/AppList/"

        # desktop data url
        desktop_response = requests.get(desktop_url, headers=headers)
        desktop_result = json.loads(desktop_response.content.decode('utf-8'))

        # app list url
        appList_response = requests.get(appList_url, headers=headers)
        appList_result = json.loads(appList_response.content.decode('utf-8'))

        if desktop_response.status_code == 404 and appList_response.status_code == 404:
            return render(request, 'push/data_to_push.html')
        elif desktop_response.status_code == 404:
            return render(request, 'push/data_to_push.html')
        else:
            pass

        if desktop_result['count'] == 0 and desktop_result['next'] is None:
            # print("no data")
            return render(request, 'push/data_to_push.html')
        elif desktop_result['count'] != 0 and desktop_result['next'] is None:
            try:
                desktop_data_to_post = {
                    "desktop_result": desktop_result,
                    "appList_result": appList_result,
                }
                try:
                    with open(os.path.join(create_desktop_directory(),
                                        randstr + str(datetime.datetime.now()) + '.json'),
                            "w") as outfile:
                        json.dump(desktop_data_to_post, outfile, indent=4, sort_keys=True)
                except Exception as bkp_error_next:
                    print("bkp error is ", bkp_error_next)
                    errorLogger.error("bkp error in desktop_data_to_post is: " + str(bkp_error_next))
                    return render(request, 'push/data_to_push.html')

            except Exception as e:
                # return False
                return render(request, 'push/data_to_push.html')
        else:
            try:
                desktop_data_to_post = {
                    "desktop_result": desktop_result,
                    "appList_result": appList_result,
                }
                try:
                    with open(os.path.join(create_desktop_directory(),
                                        randstr + str(datetime.datetime.now()) + '.json'),
                            "w") as outfile:
                        json.dump(desktop_data_to_post, outfile, indent=4, sort_keys=True)
                except Exception as bkp_error_next:
                    print("bkp error in desktop_data_to_post else part is ", bkp_error_next)
                    errorLogger.error("bkp error in desktop_data_to_post else part is: " + str(bkp_error_next))
                    return render(request, 'push/data_to_push.html')

            except Exception as e:
                print("dtp post error ", e)
                errorLogger.error("dtp post error: " + str(bkp_error_next))
                return False
            # return render(request, 'push/data_to_push.html')

        i = i+1

    return render(request, 'push/data_to_push.html')

def backupOldMethod(request):
    i = 1
    n = 6
    serial_line = ''
    randstr = ''.join(random.choice(
        string.ascii_uppercase + string.digits) for _ in range(n))

    while True:
        # usagedata backup code
        # get api
        usage_url = "http://192.168.1.16:8000/api/usagedata/?table_name=USAGEDATA&page=%s&page_size=15" % i
        print("usage_url ", usage_url)

        response = requests.get(usage_url)

        lstscore = json.loads(response.content.decode('utf-8'))

        print(response.status_code)
        if response.status_code == 404:
            return render(request, 'push/data_to_push.html')

        # pi id data to be collected
        os.system('cat /proc/cpuinfo > serial_data.txt')
        serial_file = open('serial_data.txt', "r+")
        for line in serial_file:
            if line.startswith('Serial'):
                serial_line = line

        lstscore['serial_id'] = serial_line

        if lstscore['count'] == 0 and lstscore['next'] is None:
            print("no data")
            infoLogger.info("lstscore -no data")
            return render(request, 'push/data_to_push.html')
        elif lstscore['count'] != 0 and lstscore['next'] is None:
            try:
                with open(os.path.join(create_usage_directory(),
                                       randstr + str(datetime.datetime.now()) + '.json'),
                          "w") as outfile:
                    json.dump(lstscore, outfile, indent=4, sort_keys=True)
            except Exception as bkp_error_next:
                print("bkp error in backup(request) is: ", bkp_error_next)
                errorLogger.error("bkp error in backup(request) is: " + str(bkp_error_next))
                return render(request, 'push/data_to_push.html')
        else:
            print("lstscore ", lstscore['next'])
            infoLogger.info("lstscore " + lstscore['next'])
            try:
                with open(os.path.join(create_usage_directory(),
                                       randstr + str(datetime.datetime.now()) + '.json'),
                          "w") as outfile:
                    json.dump(lstscore, outfile, indent=4, sort_keys=True)
            except Exception as bkp_error:
                print("bkp error in backup(request) else part is: ", bkp_error)
                errorLogger.error("bkp error in backup(request) else part is:" + str(bkp_error))
                return render(request, 'push/data_to_push.html')

        # desktop data backup
        desktop_url = "http://192.168.1.16:8000/api/desktopdata/?page=%s&page_size=15" % i
        appList_url = "http://192.168.1.16:8000/api/channel/AppList/"

        # desktop data url
        desktop_response = requests.get(desktop_url, headers=headers)
        desktop_result = json.loads(desktop_response.content.decode('utf-8'))

        # app list url
        appList_response = requests.get(appList_url, headers=headers)
        appList_result = json.loads(appList_response.content.decode('utf-8'))

        if desktop_response.status_code == 404 and appList_response.status_code == 404:
            return render(request, 'push/data_to_push.html')
        elif desktop_response.status_code == 404:
            return render(request, 'push/data_to_push.html')
        else:
            pass

        if desktop_result['count'] == 0 and desktop_result['next'] is None:
            # print("no data")
            return render(request, 'push/data_to_push.html')
        elif desktop_result['count'] != 0 and desktop_result['next'] is None:
            try:
                desktop_data_to_post = {
                    "desktop_result": desktop_result,
                    "appList_result": appList_result,
                }
                try:
                    with open(os.path.join(create_desktop_directory(),
                                        randstr + str(datetime.datetime.now()) + '.json'),
                            "w") as outfile:
                        json.dump(desktop_data_to_post, outfile, indent=4, sort_keys=True)
                except Exception as bkp_error_next:
                    print("bkp error is ", bkp_error_next)
                    errorLogger.error("bkp error in desktop_data_to_post is: " + str(bkp_error_next))
                    return render(request, 'push/data_to_push.html')

            except Exception as e:
                # return False
                return render(request, 'push/data_to_push.html')
        else:
            try:
                desktop_data_to_post = {
                    "desktop_result": desktop_result,
                    "appList_result": appList_result,
                }
                try:
                    with open(os.path.join(create_desktop_directory(),
                                        randstr + str(datetime.datetime.now()) + '.json'),
                            "w") as outfile:
                        json.dump(desktop_data_to_post, outfile, indent=4, sort_keys=True)
                except Exception as bkp_error_next:
                    print("bkp error in desktop_data_to_post else part is ", bkp_error_next)
                    errorLogger.error("bkp error in desktop_data_to_post else part is: " + str(bkp_error_next))
                    return render(request, 'push/data_to_push.html')

            except Exception as e:
                print("dtp post error ", e)
                errorLogger.error("dtp post error: " + str(bkp_error_next))
                return False
            # return render(request, 'push/data_to_push.html')

        i = i+1

    return render(request, 'push/data_to_push.html')


def clear_data(request):
    instance_usage = UsageData.objects.all()
    instance_usage.delete()
    instance_desktop = DeskTopData.objects.all()
    instance_desktop.delete()
    #called to delete zip files pushed from tab.
    deleteUsageZipFiles()
    #added to clear model and table data 
    instance_dbpush = DbPushData.objects.all()
    instance_dbpush.delete()
    deleteDbPushZipFiles() 
    return render(request, 'push/data_to_push.html')

#new method added to delete zip files pushed from tab after pushing to server
def deleteUsageZipFiles():
    dir = '/home/mark2/contentservermech/pos/media/usage'
    for f in os.listdir(dir):
        os.remove(os.path.join(dir,f))

#new method added to delete db zip files pushed from tab after pushing to server
def deleteDbPushZipFiles():
    dir = '/home/mark2/contentservermech/pos/media/dbpushdata'
    for f in os.listdir(dir):
        os.remove(os.path.join(dir,f))

#new method to clear UsageData model data just after pushing usage data zip from push_usageData
def clear_usage_data():
    instance_usage = UsageData.objects.all()
    instance_usage.delete()

#new method to clear DbPushData model data just after pushing dbpush data zip from push_dbpushData
def clear_dbpush_data():
    instance_dbpush = DbPushData.objects.all()
    instance_dbpush.delete()
    
#new method to clear desktop model data just after pushing desktop data to pos server
def clear_desktop_data():
    instance_desktop = DeskTopData.objects.all()
    instance_desktop.delete()

def desktop_data_to_server(request):
    print("Calling desktop_data_to_server")
    infoLogger.info("Calling desktop_data_to_server")
    print("internet connection status" , connect())
    infoLogger.info("internet connection status" +  str(connect()))
    if connect():
        i = 1
        n = 6
        #serial_line = ''
        #randstr = ''.join(random.choice(
        #    string.ascii_uppercase + string.digits) for _ in range(n))

        #if request.session.has_key('session_id'):
        #    sessionId = request.session.get('session_id')
        desktop_resultlist = []
        while True:
            # get api
            desktop_url = "http://192.168.1.16:8000/api/desktopdata/?page=%s&page_size=15" % i
            appList_url = "http://192.168.1.16:8000/api/channel/AppList/"

            # post api
            post_url = "http://rpi.prathamskills.org/api/KolibriSession/Post"

            # desktop data url
            desktop_response = requests.get(desktop_url, headers=headers)
            desktop_result = json.loads(desktop_response.content.decode('utf-8'))

            # app list url
            appList_response = requests.get(appList_url, headers=headers)
            appList_result = json.loads(appList_response.content.decode('utf-8'))

            if desktop_response.status_code == 404 and appList_response.status_code == 404:
                return render(request, 'push/data_to_push.html')
            elif desktop_response.status_code == 404:
                #commented to render data_to_push.html and added to render showpushed Data 
                #desktop_resultlist contains all data i.e. from all pages of the output of the API
                #return render(request, 'push/data_to_push.html')
                desktop_data_to_post_list = {
                        "desktop_resultlist": desktop_resultlist,                        
                    }
                # To clear desktop after pushing and after pushing to pos server
                clear_desktop_data()                    
                my_data = json.dumps(desktop_data_to_post_list)
                return render(request, 'push/showPushedDTData.html', context={"my_data": my_data})
            else:
                pass

            if desktop_result['count'] == 0 and desktop_result['next'] is None:
                # print("no data")
                return render(request, 'push/data_to_push.html')
            elif desktop_result['count'] != 0 and desktop_result['next'] is None:
                #appending desktop_result to desktop_resultlist when next is none in API result
                desktop_resultlist.append(desktop_result)
                try:
                    desktop_data_to_post = {
                        "desktop_result": desktop_result,
                        "appList_result": appList_result,
                    }
                    response_post = requests.post(
                        post_url,
                        headers=headers,
                        data=json.dumps(desktop_data_to_post),
                    )
                    #print("in desktop_data_to_server next is None")
                    print(response_post.status_code, response_post.reason)
                    # from pprint import pprint
                    # pprint(desktop_data_to_post)

                except Exception as e:
                    # return False
                    errorLogger.error("Error in desktop_data_to_server : " + str(e))
                    return render(request, 'push/data_to_push.html')
            else:
                try:
                    desktop_data_to_post = {
                        "desktop_result": desktop_result,
                        "appList_result": appList_result,
                    }
                    response_post = requests.post(
                        post_url,
                        headers=headers,
                        data=json.dumps(desktop_data_to_post),
                    )
                    #print("in desktop_data_to_server next is Nit None")
                    print(response_post.status_code, response_post.reason)
                    #appending desktop_result to desktop_resultlist when next is not none in API result
                    desktop_resultlist.append(desktop_result)
                    # from pprint import pprint
                    # pprint(desktop_data_to_post)

                except Exception as e:
                    print("dtp post error ", e)
                    errorLogger.error("dtp post error in desktop_data_to_server : " + str(e))
                    #commented return false and rendering to data_to_push instead
                    #return False
                    return render(request, 'push/data_to_push.html')
                # return render(request, 'push/data_to_push.html')

            i = i+1

        
        return render(request, 'push/data_to_push.html')
    else:
        print("when no internetconnection")
        infoLogger.info("when no internetconnection")
        return render(request, 'push/no_internet.html')    

# added to push DB Push data to pos server
def push_dbPushData(request):
    infoLogger.info("In push_dbPushData")
    infoLogger.info("internet connection status" +  str(connect()))
    if connect():
        pageNo = 1
        n = 6
        serial_line = ''
        randstr = ''.join(random.choice(
            string.ascii_uppercase + string.digits) for _ in range(n))

        while True:
            fetch_url = "http://192.168.1.16:8000/api/dbpushdata/?table_name=DBPUSHDATA&page=%s&page_size=15" % pageNo

            # post api
            post_url = "http://devprodigi.openiscool.org/api/RPIAppDB/PushFiles"

            response = requests.get(fetch_url)
            
            dbpushdata = json.loads(response.content.decode('utf-8'))
            print("dbpushdata ", dbpushdata['count'])
            infoLogger.info("dbpushdata  count" +  str(dbpushdata['count']))

            # pi id data to be collected
            os.system('cat /proc/cpuinfo > serial_data.txt')
            serial_file = open('serial_data.txt', "r+")
            for line in serial_file:
                if line.startswith('Serial'):
                    serial_line = line

            dbpushdata['serial_id'] = serial_line

            # checks the value of count
            if dbpushdata['count'] == 0 and dbpushdata['next'] is None:
                print("no data")
                infoLogger.info("no data")
                return render(request, 'push/data_to_push.html')
            elif dbpushdata['count'] != 0 and dbpushdata['next'] is None:
                try:
                    data = dbpushdata
                    print("length when next is none", len(data['results']))
                    print("data when next is  none " , data)
                    for i in range(len(data['results'])):                    
                        actualfileName = data['results'][i]["uploaded_file"]
                        print("actualfileName" ,actualfileName)
                        actualfileName = actualfileName.replace("http://192.168.1.16:8000", "/home/mark2/contentservermech/pos")
                        lastndexofFwdSlsh = actualfileName.rfind('/')                    
                        filenamestr = actualfileName[lastndexofFwdSlsh + 1:len(actualfileName)]
                        indexofDotzip = filenamestr.index(".zip")
                        filenamestr = filenamestr[0:indexofDotzip]
                        if os.path.isfile(actualfileName):
                            datasws = {filenamestr: open(actualfileName, 'rb')}
                            response_post = requests.post(post_url,files = datasws)
                            print("response_post",response_post.status_code)                       
                            infoLogger.info("response_post sws "+ str(response_post.status_code))    
                            if response_post.status_code == 200:
                                os.remove(actualfileName)                             
                        else:
                            print("Error, File "+ actualfileName +" not exists") 
                            infoLogger.info("Error, File "+ actualfileName +" not exists")  

                    # print("elif", response_post.status_code, response_post.reason)
                except Exception as bkp_error_next:
                    print("bkp error push_usageData is ", bkp_error_next)
                    errorLogger.error("bkp error push_usageData is: " + str(bkp_error_next))
                # To clear db push dat afater DB Push to pos server
                clear_dbpush_data()   
                return render(request, 'push/data_to_push.html')
            else:
                #data = lstscore  # providing lstscore value to data variable
                try:
                    data = dbpushdata  
                    print("length when next is not none", len(data['results']))
                    print("data when next is not none " , data)
                    for i in range(len(data['results'])):                    
                        actualfileName = data['results'][i]["uploaded_file"]
                        actualfileName = actualfileName.replace("http://192.168.1.16:8000", "/home/mark2/contentservermech/pos")
                        lastndexofFwdSlsh = actualfileName.rfind('/')                    
                        filenamestr = actualfileName[lastndexofFwdSlsh + 1:len(actualfileName)]
                        indexofDotzip = filenamestr.index(".zip")
                        filenamestr = filenamestr[0:indexofDotzip]
                        if os.path.isfile(actualfileName):
                            datasws = {filenamestr: open(actualfileName, 'rb')}
                            response_post = requests.post(post_url,files = datasws)
                            print("response_post sws when dbpushdata['next'] is Not None",response_post.status_code)
                            infoLogger.info("response_post sws when dbpushdata['next'] is not None "+ str(response_post.status_code))    
                            if response_post.status_code == 200:
                                os.remove(actualfileName) 
                        else:
                            print("Error, File "+ actualfileName +" not exists when dbpushdata['next'] is not None") 
                            infoLogger.info("Error, File "+ actualfileName +" not exists when dbpushdata['next'] is not None")
                    # print("el", response_post.status_code, response_post.reason)

                except Exception as e1:
                    print("error e1 is push_usageData", e1)
                    errorLogger.error("error e1 is push_usageData: " + str(e1))
                    return False
            pageNo = pageNo+1            
        return render(request, 'push/data_to_push.html')
    else:
        print("when no internetconnection")
        infoLogger.info("when no internetconnection")
        return render(request, 'push/no_internet.html')         

class NoInternetView(TemplateView):
    template_name = 'push/no_internet.html'