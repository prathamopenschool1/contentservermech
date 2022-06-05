# python and django imports
import logging
from pathlib import Path

# This retrieves a Python logging instance (or creates it)
infoLogger = logging.getLogger("info_logger")
errorLogger = logging.getLogger("error_logger")

# rest framework imports
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework.parsers import MultiPartParser, FormParser

#  filters import
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend

# local imports
from core.models import VillageDataStore, UsageData, DeskTopData,DbPushData
from .serializers import VillageDataStoreSerializer, UsageDataSerializer, DeskTopDataSerializer,DbPushDataSerializer

N = 6
# homeDir = ''

class VillageDataStoreView(viewsets.ModelViewSet):
    queryset = VillageDataStore.objects.order_by('id')
    serializer_class = VillageDataStoreSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter,)
    filter_fields = ('filter_name', 'table_name', 'key_id')
    pagination_class = PageNumberPagination


# modified to add multiparser for file upload
class UsageDataView(viewsets.ModelViewSet):
    print("inside UsageScoreFileUploadView in coreapi view ")
    infoLogger.info("inside UsageScoreFileUploadView in coreapi view ")
    model = UsageData
    queryset = UsageData.objects.all().order_by('id')
    serializer_class = UsageDataSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter)
    filter_fields = ('filter_name', 'table_name')
    pagination_class = PageNumberPagination
    parser_classes = (MultiPartParser, FormParser)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        serializer.save()

class DeskTopDataView(viewsets.ModelViewSet):
    queryset = DeskTopData.objects.order_by('id')
    serializer_class = DeskTopDataSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter,)
    filter_fields = ('node_id',)
    pagination_class = PageNumberPagination


# added for DB Push data API to call from APK 
class DbPushDataView(viewsets.ModelViewSet):
    # print("inside DbPushDataView in coreapi view ")
    infoLogger.info("inside DbPushDataView in coreapi view ")
    model = DbPushData
    queryset = DbPushData.objects.all().order_by('id')
    serializer_class = DbPushDataSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter)
    #filter_fields = ('table_name')
    filter_fields = ('filter_name', 'table_name')
    pagination_class = PageNumberPagination
    parser_classes = (MultiPartParser, FormParser)

    def create(self, request, *args, **kwargs):
        print("request.data" , request.data)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        serializer.save()

