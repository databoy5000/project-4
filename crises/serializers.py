from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from django.contrib.auth import get_user_model

from .models import Crisis, NGOResource, Request, Resource

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username')

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
            owner = validated_data['owner']
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

    # def update(self, _instance, validated_data):

    #     requests_data = validated_data.pop('requests')

    #     updated_crisis = Crisis.objects.update(
    #         disaster_type = validated_data['disaster_type'],
    #         is_solved = validated_data['is_solved'],
    #         owner = validated_data['owner']
    #     )
        
    #     requests = [
    #         Request.objects
    #             .filter(resource=request_data.get('resource'))
    #             .update(quantity=request_data.get('quantity'))
    #         for request_data in requests_data
    #     ]

    #     return updated_crisis


class NGOResourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = NGOResource
        fields = '__all__'

class PopulatedNGOResourceSerializer(NGOResourceSerializer):
    ngo_user = User()
    resource = ReadResourceSerializer()