from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import NotFound, PermissionDenied
# from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated

from .models import Crisis
from .serializers import CrisisSerializer, PopulatedCrisisSerializer

class CrisisListView(APIView):

    def get(self, _request):
        crises = Crisis.objects.all()
        serialized_crises = PopulatedCrisisSerializer(crises, many=True)
        return Response(serialized_crises.data, status=status.HTTP_200_OK)

    def post(self, request):
        new_crisis = CrisisSerializer(data=request.data)
        if new_crisis.is_valid():
            new_crisis.save()
            return Response(new_crisis.data, status=status.HTTP_201_CREATED)
        return Response(new_crisis.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY) 

class CrisisDetailView(APIView):

    def get_crisis(self, crisis_pk):
        try:
            return Crisis.objects.get(pk=crisis_pk)
        except Crisis.DoesNotExist:
            raise NotFound()

    def get(self, _request, crisis_pk):
        crisis = self.get_crisis(crisis_pk=crisis_pk)
        serialized_crisis = PopulatedCrisisSerializer(crisis)
        return Response(serialized_crisis.data, status=status.HTTP_200_OK)

    def put(self, request, crisis_pk):
        crisis_to_update = self.get_crisis(crisis_pk=crisis_pk)
        updated_crisis = CrisisSerializer(crisis_to_update, data=request.data)
        if updated_crisis.is_valid():
            updated_crisis.save()
            return Response(updated_crisis.data, status=status.HTTP_202_ACCEPTED)
        return Response(updated_crisis.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

    def delete(self, request, crisis_pk):
        crisis_to_delete = self.get_crisis(crisis_pk=crisis_pk)
        crisis_to_delete.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
