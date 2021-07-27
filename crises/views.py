from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import NotFound, PermissionDenied
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly

from .models import Crisis, NGOResource, Request, Resource
from jwt_auth.models import User
from .serializers import (
    RequestSerializer,
    WriteCrisisSerializer,
    ReadCrisisSerializer,
    ReadResourceSerializer,
    PopulatedNGOResourceSerializer,
    NGOResourceSerializer,
    CrisisSerializer
)

class CrisisListView(APIView):

    permission_classes = (IsAuthenticatedOrReadOnly, )

    def get(self, _request):
        crises = Crisis.objects.all()
        serialized_crises = ReadCrisisSerializer(crises, many=True)
        return Response(serialized_crises.data, status=status.HTTP_200_OK)

    def post(self, request):

        # * Check to only authorize Help-Seeker users to create a crisis
        user_model = User()
        model_user_types = user_model.get_user_types()
        if request.user.user_type != model_user_types[0]:
            raise PermissionDenied()

        request.data['owner'] = request.user.id
        crisis_to_create = WriteCrisisSerializer(data=request.data)

        if crisis_to_create.is_valid():
            crisis_to_create.save()
            return Response(crisis_to_create.data, status=status.HTTP_201_CREATED)

        return Response(crisis_to_create.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY) 


class CrisisDetailView(APIView):

    permission_classes = (IsAuthenticatedOrReadOnly, )

    def get_crisis(self, crisis_pk):
        try:
            return Crisis.objects.get(pk=crisis_pk)
        except Crisis.DoesNotExist:
            raise NotFound()

    def get(self, _request, crisis_pk):
        crisis = self.get_crisis(crisis_pk=crisis_pk)
        serialized_crisis = ReadCrisisSerializer(crisis)
        return Response(serialized_crisis.data, status=status.HTTP_200_OK)

    def put(self, request, crisis_pk):

        crisis_to_update = self.get_crisis(crisis_pk=crisis_pk)

        request.data['owner'] = request.user.id
        if crisis_to_update.owner != request.user:
            raise PermissionDenied()

        updated_crisis = CrisisSerializer(crisis_to_update, data=request.data)
        
        if updated_crisis.is_valid():
            updated_crisis.save()
            return Response(updated_crisis.data, status=status.HTTP_202_ACCEPTED)
        return Response(updated_crisis.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

    def delete(self, request, crisis_pk):
        crisis_to_delete = self.get_crisis(crisis_pk=crisis_pk)

        if crisis_to_delete.owner != request.user:
            raise PermissionDenied()
        
        crisis_to_delete.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class UserCrisisListView(APIView):
    
    permission_classes = (IsAuthenticatedOrReadOnly, )

    def get(self, _request, user_pk):
        user_crises = Crisis.objects.filter(owner=user_pk)

        if not user_crises:
            raise NotFound()

        serialized_crises = ReadCrisisSerializer(user_crises, many=True)
        return Response(serialized_crises.data, status=status.HTTP_200_OK)


class RequestDetailView(APIView):

    def get_crisis_request(self, crisis_request_pk):
        try:
            return Request.objects.get(pk=crisis_request_pk)
        except Request.DoesNotExist:
            raise NotFound()
            
    def put(self, request, crisis_request_pk):

        permission_classes = (IsAuthenticated, )

        crisis_request_to_update = self.get_crisis_request(crisis_request_pk=crisis_request_pk)
        crisis_owner_id = crisis_request_to_update.crisis.owner.id

        if crisis_owner_id != request.user.id:
            raise PermissionDenied()

        updated_crisis_request = RequestSerializer(
            crisis_request_to_update,
            data=request.data
        )
        
        if updated_crisis_request.is_valid():
            updated_crisis_request.save()
            return Response(updated_crisis_request.data, status=status.HTTP_202_ACCEPTED)
        return Response(updated_crisis_request.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)


class ResourceListView(APIView):

    def get(self, _request):
        resources = Resource.objects.all()
        serialized_resources = ReadResourceSerializer(resources, many=True)
        return Response(serialized_resources.data, status=status.HTTP_200_OK)


class DisasterTypesListView(APIView):

    def get(self, _request):
        crisis_model = Crisis()
        disaster_types = crisis_model.get_disaster_types()

        if disaster_types:
            return Response(disaster_types, status=status.HTTP_202_ACCEPTED)
        return Response({ "message": "Something went wrong!"}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)


class NGOResourceListView(APIView):

    permission_classes = (IsAuthenticated, )

    def get_resources(self, ngo_user):
        try:
            return NGOResource.objects.filter(ngo_user=ngo_user)
        except NGOResource.DoesNotExist:
            raise NotFound()

    def get(self, request):

        # * Check to only authorize an NGO user to get its resources
        user_model = User()
        model_user_types = user_model.get_user_types()

        if request.user.user_type != model_user_types[1]:
            raise PermissionDenied()

        ngo_resources = self.get_resources(ngo_user=request.user.id)
        serialized_ngo_resources = PopulatedNGOResourceSerializer(ngo_resources, many=True)
        return Response(serialized_ngo_resources.data, status=status.HTTP_200_OK)

    def post(self, request):
        
        present_resources = NGOResource.objects.filter(ngo_user=request.user.id)

        if len(present_resources) >= 1:
            return Response({"message": "This user already has resource entries."}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

        # * prep for serialization
        streamlined_data = []
        for resource in request.data['resources']:
            resource['ngo_user'] = request.user.id
            streamlined_data.append(resource)

        resource_to_create = NGOResourceSerializer(data=streamlined_data, many=True)

        if resource_to_create.is_valid():
            resource_to_create.save()
            return Response(resource_to_create.data, status=status.HTTP_201_CREATED)

        return Response(resource_to_create.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY) 


class NGOResourceDetailView(APIView):

    permission_classes = (IsAuthenticated, )

    def get_resource(self, resource_pk):
        try:
            return NGOResource.objects.get(pk=resource_pk)
        except NGOResource.DoesNotExist:
            raise NotFound()
    
    def put(self, request, resource_pk):

        ngo_resources_to_update = self.get_resource(resource_pk=resource_pk)

        if ngo_resources_to_update.ngo_user_id != request.user.id:
            raise PermissionDenied()

        request.data['ngo_user'] = ngo_resources_to_update.ngo_user_id

        updated_ngo_resource = NGOResourceSerializer(
            ngo_resources_to_update,
            data=request.data
        )
        
        if updated_ngo_resource.is_valid():
            updated_ngo_resource.save()
            return Response(updated_ngo_resource.data, status=status.HTTP_202_ACCEPTED)
        return Response(updated_ngo_resource.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
