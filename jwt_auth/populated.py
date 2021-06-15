from rest_framework.serializers import ModelSerializer
from django.contrib.auth import get_user_model
# from crises.serializers import CrisisSerializer

User = get_user_model()

class PopulatedUserSerializer(ModelSerializer):
    # created_crises = CrisisSerializer()

    class Meta:
        model = User
        fields = (
          'id',
          'username',
          'email',
          'profile_picture_url',
          'country',
          # 'created_crises'
        )
