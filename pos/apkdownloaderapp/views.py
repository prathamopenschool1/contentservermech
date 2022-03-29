import logging
from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import View
from modpush.pushhelper.connectcheck import PushHelper


# This retrieves a Python logging instance (or creates it)
infoLogger = logging.getLogger("info_logger")
errorLogger = logging.getLogger("error_logger")


class ApkDownloadView(View):
    psh = PushHelper()

    template_name = "apkdownloaderapp/apk_downloader.html"

    def get(self, request, *args, **kwargs):
        infoLogger.info("In push_usageData")
        infoLogger.info("internet connection status" +  str(self.psh.connect()))

        if self.psh.connect() == True:
            return render(self.request, self.template_name)
        else:
            return render(request, 'core/NoInternetFound.html')

