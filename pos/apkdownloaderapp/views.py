from re import template
from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import View


class ApkDownloadView(View):

    template_name = "apkdownloaderapp/apk_downloader.html"

    def get(self, request, *args, **kwargs):

        return render(self.request, self.template_name)

