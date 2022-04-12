import os
import json
import logging
from django.http import HttpResponse, JsonResponse
from django.views import View
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from modpush.pushhelper.connectcheck import PushHelper
from django.contrib.auth.mixins import LoginRequiredMixin
from .utils import get_data_from_api


# This retrieves a Python logging instance (or creates it)
infoLogger = logging.getLogger("info_logger")
errorLogger = logging.getLogger("error_logger")



class UpdateCheckView(LoginRequiredMixin, APIView):

    psh = PushHelper()

    def get(self, request):
        context = {}

        totalAppsList = request.GET.getlist('totalAppsList[]')
        print("total app list >>>>>> ", totalAppsList, type(totalAppsList))

        infoLogger.info("In update check view")
        infoLogger.info("internet connection status is " +  str(self.psh.connect()))

        if self.psh.connect() == True:
            get_data_from_api(totalAppsList)
            context['msg'] = 200
            return Response(context)
        else:
            context['msg'] = 500
            return Response(context)

    # def post(self, request):
    #     context = {}
    #     return Response(context, status=status.HTTP_201_CREATED)



class ApplicationUpdateView(APIView):

    psh = PushHelper()
    def post(self, request, *args, **kwargs):

        infoLogger.info("In app check view")
        infoLogger.info("internet connection status is " +  str(self.psh.connect()))

        if self.psh.connect() == True:
            context = {}
            context['msg'] = 200
            os.system('git pull origin main')
            return Response(context)
        else:
            context = {
                'msg': 500
            }
            # context = json.dumps(context)
            return Response(context)
    


    









