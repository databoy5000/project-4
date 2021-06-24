from rest_framework import serializers
from django.contrib.auth import get_user_model
import django.contrib.auth.password_validation as validations
from django.contrib.auth.hashers import make_password
from django.core.exceptions import ValidationError

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    password_confirmation = serializers.CharField(write_only=True)
    # country = serializers.CharField()
    # user_type = serializers.CharField()

    # def get_user_type(self, data):
    #     print('getting user type')
    #     print('data: ', data)


    # def validate_country(self, data):
    #     print('inside validate country')
    #     print('data: ', data)
    #     if (data.user_type == 'Help-seeker') and (not data.country or data.country == ''):
    #         raise ValidationError({'country': ['****This field may not be blank.']})

    #     return data

    def validate(self, data):
        password = data.pop('password')
        password_confirmation = data.pop('password_confirmation')

        if password != password_confirmation:
            raise ValidationError({'password_confirmation': 'Passwords do not match'})

        if (data['user_type'] == 'Help-seeker') and (not data['country'] or data['country'] == ''):
            raise ValidationError({'country': ['This field may not be blank.']})

        try:
            validations.validate_password(password=password)
        except ValidationError as err:
            raise ValidationError({'password': err.messages})

        data['password'] = make_password(password)

        return data

    class Meta:
        model = User
        fields = '__all__'
