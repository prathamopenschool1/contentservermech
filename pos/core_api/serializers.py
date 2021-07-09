from rest_framework import serializers
# imported new model DbPushData for DB Push data API
from core.models import VillageDataStore, UsageData, DeskTopData,DbPushData


class VillageDataStoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = VillageDataStore
        fields = '__all__'


class UsageDataSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        many = kwargs.pop('many', True)
        super(UsageDataSerializer, self).__init__(many=many, *args, **kwargs)

    #commneting data,filtername , tablename and adeed uploaeed_file for FileUpload in UsageAPI      
    #data = serializers.JSONField(default='\{\}')
    #filter_name = serializers.CharField(default='enter filter')
    #table_name = serializers.CharField(default='enter name')
    created_at = serializers.DateTimeField(read_only=True)
    
    # removing filter name and tablename
    #class Meta: # this is original one
    #    model = UsageData
    #    fields = (
	#		'id', 'data', 'filter_name', 'table_name', 'created_at',
    #        )
    class Meta:
        model = UsageData
        fields = (
			'id','created_at','uploaded_file',
            )


class DeskTopDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeskTopData
        fields = '__all__'


# added new serializer for new DB Push API
class DbPushDataSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        many = kwargs.pop('many', True)
        super(DbPushDataSerializer, self).__init__(many=many, *args, **kwargs)
    
    created_at = serializers.DateTimeField(read_only=True)
    
    class Meta:
        model = DbPushData
        fields = (
			'id', 'created_at','uploaded_file',
            )
