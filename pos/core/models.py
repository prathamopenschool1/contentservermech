from django.db import models
from jsonfield import JSONField
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.db.models.signals import post_save


# storing village, crl, student and group data in this model
# all the data inside this model is stored according to village selected with
# unique id of village referred as key_id
class VillageDataStore(models.Model):
    data = JSONField(default={}, blank=True)
    filter_name = models.CharField(max_length=100, default="Enter filter name")
    table_name = models.CharField(max_length=100, default="Enter table name")
    key_id = models.CharField(max_length=50, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    @classmethod
    def create(cls, data, filter_name, table_name, key_id):
        village_data = cls(data=data, filter_name=filter_name,
                           table_name=table_name, key_id=key_id)
        return village_data


class UsageData(models.Model):
    data = JSONField(default={}, blank=True)
    filter_name = models.CharField(max_length=100, default="Enter filter name")
    #added new column for new field uploaded_file and changed deafult=USAGEDATA in pushing usage data API to be used from APK
    #table_name = models.CharField(max_length=100, default="Enter table name")
    table_name = models.CharField(max_length=100, default="USAGEDATA")
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    uploaded_file = models.FileField(upload_to='usage/')
   


class DeskTopData(models.Model):
    session_id = models.CharField(max_length=30, default="")
    node_id = models.CharField(max_length=100, default="")
    start_time = models.CharField(max_length=100, default="")
    end_time = models.CharField(max_length=100, default="")
    duration = models.CharField(max_length=100, default="")
    user = models.CharField(max_length=100, default="")
    serial_id = models.CharField(max_length=50, default="", null=True, blank=True)

    @classmethod
    def create(cls, session_id, node_id, start_time, end_time, duration, user, serial_id):
        desktop_data = cls(session_id=session_id, node_id=node_id, start_time=start_time, 
                            end_time=end_time, duration=duration, user=user,
                            serial_id=serial_id)
        return desktop_data
        
        

#added new model for saving DB Push details received from android app
class DbPushData(models.Model):
    filter_name = models.CharField(max_length=100, default="Enter filter name")
    table_name = models.CharField(max_length=100, default="DBPUSHDATA")
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)    
    uploaded_file = models.FileField(upload_to='dbpushdata/')


