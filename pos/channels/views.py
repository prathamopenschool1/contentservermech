import os
import json
import time
import requests
import logging
from pathlib import Path
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.views.generic import View, TemplateView, ListView
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from .models import (AppAvailableInDB, AppListFromServerData,
                     FileDataToBeStored, JsonDataStorage)

# rest framework imports
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view

# command line progress bar import
from clint.textui import progress

from datetime import datetime

#custom imports
from channels.file_downloader import Downloader

# creating object of Downloader class
downloading = Downloader()

# This retrieves a Python logging instance (or creates it)
infoLogger = logging.getLogger("info_logger")
errorLogger = logging.getLogger("error_logger")

# home directory check for every os
homeDir = str(Path.home())

# headers for data fetching
headers = {
    'cache-control': "no-cache",
    'content-type': "application/json; charset=utf-8",
    "Accept": "application/json"
}

channels_result = None

# getting list of channels using API
@login_required
def channel_list_on_server(request):
    # global channels_result
    try:
        context = {}
        channels_url = "http://devposapi.prathamopenschool.org/api/AppList"
        channels_response = requests.get(channels_url, headers=headers)
        channels_result = json.loads(channels_response.content.decode("utf-8"))
        for app in  channels_result:
            for k,v in app.items():
                if k == 'AppName':
                    downloading.download_files_without_qs(channels_url, v)
        context['channels_from_server'] = channels_result
        return render(request, 'channels/channels_list_from_server.html', context=context)
    except requests.exceptions.ConnectionError as err_channel_list_on_server:
        errorLogger.error("error-channel_list_on_server: " + str(err_channel_list_on_server))
        return HttpResponseRedirect('/channel/no_internet/')


# return the json response in api form for showing checkboxes nad details
@api_view(['GET'])
def return_json_value(request, AppId):
    try:
        url_to_convert = "http://devposapi.prathamopenschool.org/api/AppNode?id={}" .format(
            AppId)
        response_url = requests.get(url_to_convert, headers=headers)
        result_url = json.loads(response_url.content.decode('utf-8'))
        context = {
            'json_data': result_url,
        }
        return Response(context, status=status.HTTP_200_OK)
    except requests.exceptions.ConnectionError as err_return_json_value:
        errorLogger.error("error-return_json_value: " + str(err_return_json_value))
        return HttpResponseRedirect('/channel/no_internet/')


# showing the page to downlaod the content (jsondata and files)
class ShowDetailsOfChannelView(LoginRequiredMixin, View):
    template_name = "channels/show_details.html"

    def get(self, request, AppId, AppName, *args, **kwargs):
        try:
            context = {}
            # print("my app id and name ", AppId, AppName)
            infoLogger.info("AppId,AppName in ShowDetailsOfChannelView - AppId: " + AppId + "AppName: " + AppName )
            context['AppId'] = AppId
            context['AppName'] = AppName
            # filed_query = FileDataToBeStored.objects.all().values_list('NodeId', flat=True).distinct()
            # filed_query = json.dumps(list(filed_query))
            # print("filed_query is ", filed_query)
            appAvail_query = AppAvailableInDB.objects.filter(NodeType="Resource").values_list('NodeId', flat=True).distinct()
            appAvail_query = json.dumps(list(appAvail_query))
            # print("app query  is ", appAvail_query, type(appAvail_query))
            context['appAvail_query'] = appAvail_query
            return render(self.request, self.template_name, context=context)
        except requests.exceptions.ConnectionError as  sdlcvConnectionError :
            errorLogger.error("error-ShowDetailsOfChannelView:" + str(sdlcvConnectionError))
            return HttpResponseRedirect('/channel/no_internet/')


# Downloading and saving the jsondata and files with ids
class DownloadAndSaveView(LoginRequiredMixin, View):

    def post(self, request, *args, **kwargs):
        node_values = request.POST.getlist('node_values[]')
        AppId = request.POST.get('AppId')
        AppName = request.POST.get('AppName')

        channels_url = "http://devposapi.prathamopenschool.org/api/AppList"
        channels_response = requests.get(channels_url, headers=headers)
        channels_result = json.loads(channels_response.content.decode("utf-8"))

        """ downloading and saving the content from here
            looping through node_values list"""
        # applist_server_data = None
        startTime = datetime.now()
        print("starting DownloadAndSaveView at " , startTime);
        infoLogger.info("starting DownloadAndSaveView at " + str(startTime))
        if not AppListFromServerData.objects.filter(AppId=AppId).exists():
            print(AppId, "server data not in db")
            infoLogger.info(AppId + "server data not in db")
            for apps in channels_result:
                if apps["AppId"] == AppId:
                    applist_local_url = downloading.localUrl
                    applist_local_url = applist_local_url.split('static')[1]
                    print("local url is ", 'static'+applist_local_url)
                    applist_local_url = 'static'+applist_local_url
                    AppId = apps["AppId"]
                    AppName = apps['AppName']
                    ThumbUrl = apps['ThumbUrl']
                    AppDesc = apps['AppDesc']
                    AppOrder = apps['AppOrder']
                    DateUpdated = apps['DateUpdated']
                    fileName = os.path.basename(ThumbUrl)
                    localUrl = applist_local_url
                    # print("filename", fileName)
                    applist_server_data = AppListFromServerData.objects.create(AppId=AppId, AppName=AppName,
                                                                               ThumbUrl=ThumbUrl, AppDesc=AppDesc,
                                                                               AppOrder=AppOrder, DateUpdated=DateUpdated,
                                                                               fileName=fileName,
                                                                               localUrl=applist_local_url)
                    applist_server_data.save()
        else:
            # just pass the instance of existing app with app id
            applist_server_data = AppListFromServerData.objects.only(
                'AppId').get(AppId=AppId)

        for ids in node_values:
            # hit the detail node each time and get the result
            try:
                detail_node_url = "http://devposapi.prathamopenschool.org/Api/AppNodeDetailListByNode?id={}" .format(
                    ids)
                detail_node_response = requests.get(
                    detail_node_url, headers=headers, timeout=13)
                detail_node_json_val = json.loads(
                    detail_node_response.content.decode('utf-8'))

                # downloading the files
                response_data = downloading.download_files_with_qs(detail_node_url, {"id": ids}, AppName)

                if response_data is False:
                    return HttpResponse('Failed')
                else:
                    # print("localUrl is ", downloading.localUrl)
                    local_url = downloading.localUrl
                    local_url = local_url.split('static')[1]
                    print("local url is ", 'static'+local_url, local_url)
                    local_url = 'static'+local_url
                    for detail in detail_node_json_val:
                        try:
                            NodeId = detail['NodeId']
                            NodeType = detail['NodeType']
                            NodeTitle = detail['NodeTitle']
                            JsonData = detail['JsonData']
                            ParentId = detail['ParentId']
                            AppId = detail['AppId']
                            DateUpdated = detail['DateUpdated']
                            if AppAvailableInDB.objects.filter(NodeId=NodeId).exists():
                                AppAvailableInDB.objects.filter(NodeId=NodeId).delete()
                            app_in_db = AppAvailableInDB.objects.create(applistfromserverdata=applist_server_data,
                                                                        NodeId=NodeId, NodeType=NodeType, NodeTitle=NodeTitle,
                                                                        JsonData=JsonData, ParentId=ParentId,  AppId=AppId,
                                                                        DateUpdated=DateUpdated)
                            app_in_db.save()
                            start = time.time()
                            for file in detail["LstFileList"]:
                                print("file data is ", file)
                                FileId = file['FileId']
                                NodeId = file['NodeId']
                                FileType = file['FileType']
                                FileUrl = file['FileUrl']
                                DateUpdated = file['DateUpdated']
                                fileName = os.path.basename(FileUrl)
                                localUrl = local_url
                                infoLogger.info("file data is " + str(file))
                                #infoLogger.info("file data is : FileId :" + FileId + " ,NodeId :" + NodeId + " ,FileType :" + FileType +" ,fileName, :" + fileName + " ,localUrl, :" + localUrl)
                                if FileDataToBeStored.objects.filter(NodeId=NodeId, FileId=FileId).exists():
                                    FileDataToBeStored.objects.filter(NodeId=NodeId, FileId=FileId).delete()
                                file_in_db = FileDataToBeStored.objects.create(appavailableindb=app_in_db,
                                                                                FileId=FileId, NodeId=NodeId,
                                                                                FileType=FileType, FileUrl=FileUrl,
                                                                                DateUpdated=DateUpdated, 
                                                                                fileName=fileName,
                                                                                localUrl=local_url)
                                file_in_db.save()
                                    
                        except requests.exceptions.ConnectionError as connecton_err1:
                            endTimeInExceptionDbErr = datetime.now()
                            errorLogger.error("Exception - dberror occured at DownloadAndSaveView at " +str(endTimeInExceptionDbErr))
                            time_taken_exceptiondberr = endTimeInExceptionDbErr - startTime
                            errorLogger.error('Time Taken to till db err exception got in DownloadAndSaveView: '+ str(time_taken_exceptiondberr)) 
                            errorLogger.error("db error - Loop- detail in detail_node_json_val :" + str(connecton_err1))
                            return HttpResponseRedirect('/channel/no_internet/')
                
                json_data_storage_view(request, ids)

            except requests.exceptions.ConnectionError as connecton_err2:
                endTimeInException = datetime.now()
                errorLogger.error("Exception occured at DownloadAndSaveView at " + str(endTimeInException))
                time_taken_exception = endTimeInException - startTime
                errorLogger.error('Time Taken to till downlaod error got in DownloadAndSaveView: '+str(time_taken_exception)) 
                errorLogger.error("downlaod error - Loop- ids in node_values :" + str(connecton_err2))
                #commented redirect to no_internet to continue downloading after internet is up again and added continue below
                #return HttpResponseRedirect('/channel/no_internet/')
                # continue
                return HttpResponse("Failed")

        # return HttpResponse("success!!")
        endTime = datetime.now()
        infoLogger.info("Ending DownloadAndSaveView at " + str(endTime))
        time_taken = endTime - startTime
        infoLogger.info('Time Taken to complete DownloadAndSaveView: '+ str(time_taken)) 
        infoLogger.info("successfully saved!")
        return HttpResponse("success")


def json_data_storage_view(request, id):
    json_url = "http://devposapi.prathamopenschool.org/api/AppNodeJsonListByNode?id=%s" % id
    json_response = requests.get(json_url, headers=headers)
    json_result = json.loads(json_response.content.decode("utf-8"))

    try:
        for result in json_result:
            JsonId = result['JsonId']
            NodeId = result['NodeId']
            JsonType = result['JsonType']
            JsonData = result['JsonData']
            DateUpdated = result['DateUpdated']

            if JsonDataStorage.objects.filter(NodeId=NodeId, JsonType=JsonType).exists():
                JsonDataStorage.objects.filter(NodeId=NodeId, JsonType=JsonType).delete()
            json_data_storage = JsonDataStorage.objects.create(JsonId=JsonId, NodeId=NodeId, JsonType=JsonType, JsonData=JsonData,
                                                                DateUpdated=DateUpdated)
            json_data_storage.save()
    
    except requests.exceptions.ConnectionError as con_err:
        errorLogger.error("json error :" + str(con_err))
        return HttpResponseRedirect('/channel/no_internet/')

    return HttpResponse(json_result)


class NoInternetView(TemplateView):
    template_name = 'channels/no_internet.html'


# def download_confirmor_mtd(request):
    
#     return HttpResponse("download confirmed!!!")


