import os, time
import platform
import logging
from pathlib import Path
from itertools import chain
from django.http import HttpResponse
from django.http.response import FileResponse
from content_viewer.extracter import extraction
from content_viewer.converter import m4v_to_mp4, wav_to_mp3
from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView, ListView, DetailView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.sessions.models import Session
from core.models import DeskTopData
from channels.models import AppListFromServerData, AppAvailableInDB, FileDataToBeStored


system_os = platform.system()

from django.http import HttpResponse

# This retrieves a Python logging instance (or creates it)
infoLogger = logging.getLogger("info_logger")
errorLogger = logging.getLogger("error_logger")

# checking the list of available apps
class AppAvailableListView(ListView):
    model = AppListFromServerData
    template_name = "content_viewer/app_available.html"

    def get_queryset(self, *args, **kwargs):
        queryset = AppListFromServerData.objects.all()
        return queryset

    def get_context_data(self, *args, **kwargs):
        context = super(AppAvailableListView, self).get_context_data(*args, **kwargs)
        queryset = self.get_queryset()
        context["apps_list"] = queryset
        infoLogger.info("In get_context_data!!")
        return context


class ParentAppView(ListView):
    # model = AppAvailableInDB
    template_name = "content_viewer/app_details.html"

    def get_queryset(self, *args, **kwargs):
        AppId = self.kwargs['AppId']
        self.request.session['AppId'] = AppId
        infoLogger.info("AppId is " + AppId)
        queryset = FileDataToBeStored.objects.all().select_related('appavailableindb').filter(appavailableindb__AppId=AppId)
        return queryset

    def get_context_data(self, *args, **kwargs):
        infoLogger.info("AppId is " + self.request.session.get('AppId'))
        context = super(ParentAppView, self).get_context_data(*args, **kwargs)
        queryset = self.get_queryset()
        folder_app_name = AppListFromServerData.objects.filter(AppId=self.request.session.get('AppId'))
        for app in folder_app_name:
            infoLogger.info("app.AppName " + app.AppName)
            self.request.session['folder_app_name'] = app.AppName
        context['folder_app_name'] = self.request.session.get('folder_app_name')
        context["parent_details"] = queryset
        return context


class ChildrenAppView(ListView):
    template_name = "content_viewer/child_details.html"

    def get_queryset(self, *args, **kwargs):
        # global NodeId
        NodeId = self.kwargs['NodeId']
        self.request.session['NodeId'] = NodeId
        # print("child NodeId is ", self.request.session.get('NodeId'))
        infoLogger.info("child NodeId is "+ self.request.session.get('NodeId'))
        queryset = FileDataToBeStored.objects.all().prefetch_related('appavailableindb').filter(appavailableindb__ParentId=NodeId)
        return queryset

    def get_context_data(self, *args, **kwargs):
        context = super(ChildrenAppView, self).get_context_data(*args, **kwargs)
        queryset = self.get_queryset()
        app_name = AppListFromServerData.objects.all()
        parent_db = AppAvailableInDB.objects.filter(NodeId=self.request.session.get('NodeId'))
        parent_db_title = AppAvailableInDB.objects.filter(NodeId=self.request.session.get('NodeId'))
        combined_results = ''
        chaining_queries = []
    
        while parent_db:
            parent_id = parent_db.first().ParentId
            parent_db = AppAvailableInDB.objects.filter(NodeId=parent_id)
            if not parent_db:
                pass
            else:
                parent_db = AppAvailableInDB.objects.filter(NodeId=parent_id)
                chaining_queries.append(parent_db)
        combined_results = list(chain(chaining_queries[::-1]))
        context['chaining_queries'] = combined_results
        context['app_name'] = app_name
        context['child_details'] = queryset
        context['appid'] = self.request.session.get('AppId')
        # print(context)
        context['parent_db_title'] = parent_db_title
        return context


def resource_view(request, NodeId):
    context = {}
    queryset = FileDataToBeStored.objects.filter(NodeId=NodeId)
    zip_path = os.getcwd()
    general_path = os.getcwd()
    app_name = AppListFromServerData.objects.all()
    parent_db = AppAvailableInDB.objects.filter(NodeId=NodeId)
    parent_db_title = AppAvailableInDB.objects.filter(NodeId=NodeId)
    combined_results = ''
    chaining_queries = []
        
    while parent_db:
        parent_id = parent_db.first().ParentId
        parent_db = AppAvailableInDB.objects.filter(NodeId=parent_id)
        if not parent_db:
            pass
        else:
            parent_db = AppAvailableInDB.objects.filter(NodeId=parent_id)
            chaining_queries.append(parent_db)
    
    combined_results = list(chain(chaining_queries[::-1]))
    context['chaining_queries'] = combined_results
    context['app_name'] = app_name
    context['node_id'] = NodeId
    context['appid'] = request.session.get('AppId')
    context['parent_db_title'] = parent_db_title
    # print("genral path is ", general_path, zip_path)
    infoLogger.info("general path is " +  general_path + " and zip path is " +  zip_path)
    zip_path = os.path.join(zip_path, 'storage'+'/'+request.session.get('folder_app_name')+'/'+'content/zips')
    vid_m4v_path = os.path.join(general_path, 'storage/'+request.session.get('folder_app_name')+'/content/videos/m4v')
    # print("vid_m4v_path path is ", vid_m4v_path, zip_path)
    audio_wav_path = os.path.join(general_path, 'storage'+'/'+request.session.get('folder_app_name')+'/'+'content/audios/wav')
    # print("audio_wav_path path is ", audio_wav_path, zip_path)
    for qs in queryset:
        if qs.FileType == "Content" and qs.fileName.endswith('.zip'):
            zip_path1 = os.path.join(zip_path, qs.fileName)
            qs.fileName = extraction(zip_path1, request.session.get('folder_app_name'))
            if qs.fileName == '-1':
                context['bad_file'] = "This file is not a proper zip file!!"
                return render(request, "content_viewer/content_play.html", context=context)
            elif qs.fileName == '-2':
                context['android_file'] = "This File can only be played on Android Devices!"
                return render(request, "content_viewer/content_play.html", context=context)
            else:
                zip_path = os.path.join(zip_path, qs.fileName)
                context['file'] = qs.fileName
                context['game_play'] = queryset
                return render(request, "content_viewer/content_play.html", context=context)
                
        elif qs.FileType == "Content" and qs.fileName.endswith('.mp4'):
            context['video_play'] = queryset
            return render(request, "content_viewer/content_play.html", context=context)
        elif qs.FileType == "Content" and qs.fileName == '':
            context['no_content'] = queryset
            return render(request, "content_viewer/content_play.html", context=context)
        elif qs.FileType == "Content" and qs.fileName.endswith('.m4v'):
            vid_m4v_path1 = os.path.join(vid_m4v_path, qs.fileName)
            qs.fileName = m4v_to_mp4(vid_m4v_path1, request.session.get('folder_app_name'))
            if system_os == "Windows":
                converted_video = qs.fileName.split('\\')[-1]
            else:
                converted_video = qs.fileName.split('/')[-1]
            context['m4v_video_play'] = queryset
            context['converted_video'] = converted_video
            return render(request, "content_viewer/content_play.html", context=context)
        elif qs.FileType == "Content" and qs.fileName.endswith('.mp3'):
            context['audio_play'] = queryset
            return render(request, "content_viewer/content_play.html", context=context)
        elif qs.FileType == "Content" and qs.fileName.endswith('.wav'):
            audio_wav_path1 = os.path.join(audio_wav_path, qs.fileName)
            qs.fileName = wav_to_mp3(audio_wav_path1, request.session.get('folder_app_name'))
            if system_os == "Windows":
                converted_audio = qs.fileName.split('\\')[-1]
            else:
                converted_audio = qs.fileName.split('/')[-1]
            context['wav_audio_play'] = queryset
            context['converted_audio'] = converted_audio
            return render(request, "content_viewer/content_play.html", context=context)
        elif qs.FileType == "Content" and qs.fileName.endswith('.png' or '.jpg' or '.jpeg' or '.mpeg'):
            context['wrong_format'] = queryset
            return render(request, "content_viewer/content_play.html", context=context)
        elif qs.FileType == "Content" and qs.fileName.endswith('.pdf'):
            if request.user_agent.is_mobile or request.user_agent.is_tablet:
                pdf_file_path = os.path.join(general_path, 'storage/'+str(request.session.get('folder_app_name'))+'/content/docs')
                pdf_file_path = os.path.join(pdf_file_path, qs.fileName)
                return FileResponse(open(pdf_file_path, 'rb'), as_attachment=True, content_type='application/pdf')
            else:
                context['pdf_play'] = queryset
                return render(request, "content_viewer/content_play.html", context=context)


def desktop_score_data(request):
    if request.method == 'GET':
        try:
            node_id = request.GET.get('NodeId')
            startTime = request.GET.get('startTime')
            endTime = request.GET.get('endTime')
            duration = request.GET.get('duration')
            user = request.user
            if user.is_authenticated:
                logged_in_user = user.username
            else:
                logged_in_user = "guest"

            infoLogger.info("logged_in_user is " +logged_in_user)    

            # pi id data to be collected
            os.system('cat /proc/cpuinfo > serial_data.txt')
            serial_file = open('serial_data.txt', "r+")
            for line in serial_file:
                if line.startswith('Serial'):
                    serial_id = line.split(':')[1]
                    break
                else:
                    serial_id = ""

            if request.session.has_key('session_id'):
                session_id = request.session.get('session_id')

            DeskTopData.objects.create(session_id=session_id, node_id=node_id, start_time=startTime, 
                                                      end_time=endTime, duration=duration, user=user,
                                                      serial_id=serial_id)
        except Exception as e:
            print("desktop save error is ", e)
            errorLogger.error("Error in desktop_score_data is " + str(e))
            return False
    return HttpResponse("success")
