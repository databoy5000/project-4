from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import NotFound, PermissionDenied
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly

from .models import Crisis, Resource
from .serializers import WriteCrisisSerializer, ReadCrisisSerializer, ReadResourceSerializer


class CrisisListView(APIView):

    permission_classes = (IsAuthenticatedOrReadOnly, )

    def get(self, _request):
        crises = Crisis.objects.all()
        serialized_crises = ReadCrisisSerializer(crises, many=True)
        return Response(serialized_crises.data, status=status.HTTP_200_OK)

    def post(self, request):
        
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

        if crisis_to_update.owner != request.user:
            raise PermissionDenied()

        request.data['owner'] = request.user.id
        updated_crisis = WriteCrisisSerializer(crisis_to_update, data=request.data)
        
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


class ResourceListView(APIView):

    def get(self, _request):
        resources = Resource.objects.all()
        serialized_resources = ReadResourceSerializer(resources, many=True)
        return Response(serialized_resources.data, status=status.HTTP_200_OK)

# ! check all the below
class NGOResourceDetailView(APIView):

    permission_classes = (IsAuthenticated, )

    def get_crisis(self, crisis_pk):
        try:
            return Crisis.objects.get(pk=crisis_pk)
        except Crisis.DoesNotExist:
            raise NotFound()

    def get(self, _request, crisis_pk):
        request.data['owner'] = request.user.id
        crisis = self.get_crisis(crisis_pk=crisis_pk)
        serialized_crisis = ReadCrisisSerializer(crisis)
        return Response(serialized_crisis.data, status=status.HTTP_200_OK)