import os
import logging
from django.views import View
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from modpush.pushhelper.connectcheck import PushHelper
from django.contrib.auth.mixins import LoginRequiredMixin


# This retrieves a Python logging instance (or creates it)
infoLogger = logging.getLogger("info_logger")
errorLogger = logging.getLogger("error_logger")



class UpdateCheckView(LoginRequiredMixin, APIView):

    psh = PushHelper()

    def get(self, request):
        context = {}

        totalAppsList = request.GET.getlist('totalAppsList[]')

        infoLogger.info("In push_usageData")
        infoLogger.info("internet connection status is " +  str(self.psh.connect()))

        if self.psh.connect() == True:
            context['msg'] = 200
            return Response(context)
        else:
            context['msg'] = 500
            return Response(context)

    # def post(self, request):
    #     context = {}
    #     return Response(context, status=status.HTTP_201_CREATED)


    









