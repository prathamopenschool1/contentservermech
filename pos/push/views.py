import os,shutil
import json
import string
import random
import platform
import datetime
import requests
import time
import logging
from pathlib import Path
from django.contrib import messages
from core.models import UsageData, DeskTopData
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
print(system_os)
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


def push_usageData(request):
    i = 1
    #n = 6
    serial_line = ''
    #randstr = ''.join(random.choice(
    #    string.ascii_uppercase + string.digits) for _ in range(n))

    while True:
        fetch_url = "http://192.168.4.1:8000/api/usagedata/?table_name=USAGEDATA&page=%s&page_size=15" % i

        # post api
        #commeted out to use new API for zip upload 
        #post_url = "http://rpi.prathamskills.org/api/KolibriSession/Post"
        post_url = "http://devprodigi.openiscool.org/api/RPIAppZipPush/PushFiles"

        response = requests.get(fetch_url)

        lstscore = json.loads(response.content.decode('utf-8'))
        print("lstscore ", lstscore['count'])

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
                    actualfileName = actualfileName.replace("http://192.168.4.1:8000", "/home/pi/contentservermech/pos")
                    lastndexofFwdSlsh = actualfileName.rfind('/')                    
                    filenamestr = actualfileName[lastndexofFwdSlsh + 1:len(actualfileName)]
                    indexofDotzip = filenamestr.index(".zip")
                    filenamestr = filenamestr[0:indexofDotzip]
                    if os.path.isfile(actualfileName):
                       datasws = {filenamestr: open(actualfileName, 'rb')}
                       response_post = requests.post(post_url,files = datasws)
                       print("response_post sws ",response_post.status_code)
                       infoLogger.info("response_post sws "+ str(response_post.status_code))    
                       if response_post.status_code == 200:
                          os.remove(actualfileName) 
                          
                    else:
                       print("Error, File "+ actualfileName +" not exists") 
                       infoLogger.info("Error, File "+ actualfileName +" not exists")       
                """ response_post = requests.post(
                    post_url,
                    headers=headers,   # modified for usagedata
                    #headers=headers_ForUsage,
                    data=json.dumps(data),
                ) """
                
            except Exception as bkp_error_next:
                print("error push_usageData is ", bkp_error_next)
                errorLogger.error("Error push_usageData is: " + str(bkp_error_next))
            return render(request, 'push/data_to_push.html')
        else:
            
            try:
                data = lstscore  # providing lstscore value to data variable
                print("length", len(data['results']))
                print("data " , data)
                for i in range(len(data['results'])):                    
                    actualfileName = data['results'][i]["uploaded_file"]
                    actualfileName = actualfileName.replace("http://192.168.4.1:8000", "/home/pi/contentservermech/pos")
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
                """ response_post = requests.post(
                    post_url,
                    headers=headers,
                    data=json.dumps(data),
                ) """
                
            except Exception as e1:
                print("Error in push_usageData when lstscore['next'] is not None: ", e1)
                errorLogger.error("Error in push_usageData when lstscore['next'] is not None: " + str(e1))
                return False
        i = i+1
    return render(request, 'push/data_to_push.html')

def backup(request):
    
    i = 1
    n = 6
    #serial_line = ''
    randstr = ''.join(random.choice(
        string.ascii_uppercase + string.digits) for _ in range(n))

    destDir = os.path.join(create_usage_directory(),
             randstr + str(datetime.datetime.now()))
    
    srcDir = '/home/pi/contentservermech/pos/media/usage'     

    if os.listdir(srcDir):    
        shutil.copytree(srcDir, destDir, symlinks = True)    

    while True:        

        # desktop data backup
        desktop_url = "http://192.168.4.1:8000/api/desktopdata/?page=%s&page_size=15" % i
        appList_url = "http://192.168.4.1:8000/api/channel/AppList/"

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
        usage_url = "http://192.168.4.1:8000/api/usagedata/?table_name=USAGEDATA&page=%s&page_size=15" % i
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
        desktop_url = "http://192.168.4.1:8000/api/desktopdata/?page=%s&page_size=15" % i
        appList_url = "http://192.168.4.1:8000/api/channel/AppList/"

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
    return render(request, 'push/data_to_push.html')

#new method added to delete zip files pushed from tab.
def deleteUsageZipFiles():
    dir = '/home/pi/contentservermech/pos/media/usage'
    for f in os.listdir(dir):
        os.remove(os.path.join(dir,f))


def desktop_data_to_server(request):
    print("Calling desktop_data_to_server")
    infoLogger.info("Calling desktop_data_to_server")
    print("internet connection status" , connect())
    if connect():
        i = 1
        n = 6
        desktop_resultlist = []
        serial_line = ''
        randstr = ''.join(random.choice(
            string.ascii_uppercase + string.digits) for _ in range(n))

        if request.session.has_key('session_id'):
            sessionId = request.session.get('session_id')

        while True:
            # get api
            desktop_url = "http://192.168.4.1:8000/api/desktopdata/?page=%s&page_size=15" % i
            appList_url = "http://192.168.4.1:8000/api/channel/AppList/"

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
        print("No internet connection")
        infoLogger.info("No internetconnection")
        return render(request, 'push/no_internet.html')

class NoInternetView(TemplateView):
    template_name = 'push/no_internet.html'              

