import os
import json
import logging
import requests
from django.shortcuts import render
from django.views.generic import View
from django.views.generic.base import TemplateView
from django.http import JsonResponse, HttpResponse
from modpush.pushhelper.connectcheck import PushHelper


# This retrieves a Python logging instance (or creates it)
infoLogger = logging.getLogger("info_logger")
errorLogger = logging.getLogger("error_logger")


class ApkPageServeView(TemplateView):
    template_name = "apkdownloaderapp/apk_downloader.html"


class ApkDownloadView(View):
    psh = PushHelper()
    
    def post(self, request, *args, **kwargs):
        host = request.POST.get('idValue')
        infoLogger.info("In push_usageData")
        infoLogger.info(f"internet connection status{str(self.psh.connect(host=host))}")

        if self.psh.connect(host=host) == True:
            apk_name = os.path.basename(host)
            apk_path = '/var/www/html/data/'
            if os.path.exists(apk_path):
                os.system('sudo chmod 777 -R /var/www/html/index/data/')
                dwn_Apk = requests.get(host, stream=True)
                with open(os.path.join(apk_path, apk_name), "wb") as apkWrite:
                    apkWrite.write(dwn_Apk.content)
                context = {'msg': 200}
            else:
                context = {'msg': 303}
            context = json.dumps(context)
        else:
            context = {'msg': 701}
            context = json.dumps(context)
            errorLogger.error("Internet is not Working!!")

        return JsonResponse(context, safe=False)

