from rest_framework import serializers
from .models import Crisis, NGOResource, Request

class RequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Request
        fields = '__all__'

class CrisisSerializer(serializers.ModelSerializer):
    class Meta:
        model = Crisis
        fields = '__all__'

class NGOResourceSerializer(CrisisSerializer):
    class Meta:
        model = NGOResource
        fields = '__all__'

class PopulatedCrisisSerializer(CrisisSerializer):
    requests = RequestSerializer(many=True)

class PopulatedNGOResourceSerializer(CrisisSerializer):
    ngo_resources = NGOResourceSerializer(many=True)