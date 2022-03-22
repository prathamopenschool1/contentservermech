from curses.ascii import HT
from django.shortcuts import render
from django.http import HttpResponse


def apk_index(request):

    return HttpResponse("This is apks download page bro")

