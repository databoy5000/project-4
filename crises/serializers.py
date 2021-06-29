from rest_framework import serializers
from django.contrib.auth import get_user_model

from .models import Crisis, NGOResource, Request, Resource

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'profile_picture_url')

class ReadResourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resource
        fields = '__all__'

class RequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Request
        fields = ('id', 'quantity', 'resource')

class PopulatedReadRequestSerializer(RequestSerializer):
    resource = ReadResourceSerializer()

class CrisisSerializer(serializers.ModelSerializer):
    class Meta:
        model = Crisis
        fields = '__all__'

class ReadCrisisSerializer(CrisisSerializer):
    requests = PopulatedReadRequestSerializer(many=True)
    owner = UserSerializer()

class WriteCrisisSerializer(CrisisSerializer):
    requests = RequestSerializer(many=True)

    def create(self, validated_data):
        requests_data = validated_data.pop('requests')
        created_crisis = Crisis.objects.create(
            disaster_type = validated_data['disaster_type'],
            is_solved = validated_data['is_solved'],
            owner = validated_data['owner'],
            longitude = validated_data['longitude'],
            latitude = validated_data['latitude'],
            place_name = validated_data['place_name'],
            country = validated_data['country'],
            disaster_description = validated_data['disaster_description'],
            place_type = validated_data['place_type']
        )
        
        requests = [
            Request.objects.create(
                crisis = created_crisis,
                quantity = request_data.get('quantity'),
                resource = request_data.get('resource'),
            )
            for request_data in requests_data
        ]

        return created_crisis

class NGOResourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = NGOResource
        fields = '__all__'

class PopulatedNGOResourceSerializer(NGOResourceSerializer):
    ngo_user = User()
    resource = ReadResourceSerializer()