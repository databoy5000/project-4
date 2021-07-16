from datetime import datetime, timedelta
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied, NotFound, ValidationError
from rest_framework import status
from django.contrib.auth import get_user_model
from django.conf import settings
import jwt

from .serializers import UserSerializer
from .populated import PopulatedUserSerializer

User = get_user_model()

class RegisterView(APIView):

    def new_user_token(self, new_user):
        expiry_time = datetime.now() + timedelta(days=7)
        token = jwt.encode(
            {
                'sub': new_user['id'],
                'exp':  int(expiry_time.strftime('%s')),
                'type': new_user['user_type']
            },
            settings.SECRET_KEY, 
            algorithm='HS256'
        )

        return token

    def post(self, request):
        user_to_create = UserSerializer(data=request.data)
        if user_to_create.is_valid():
            if request.data['user_type'] == 'Help-seeker':
                try:
                    User.objects.get(country=request.data['country'])
                except User.DoesNotExist:
                    user_to_create.save()
                    token = self.new_user_token(new_user=user_to_create.data)
                    return Response(
                        {
                            'message': 'Registration successful',
                            'token': token
                        },
                        status=status.HTTP_201_CREATED
                    )
                return Response({'country': ['Help seeker already exists for this country.']}, status=status.HTTP_409_CONFLICT)
            else:
                user_to_create.save()
                token = self.new_user_token(new_user=user_to_create.data)
                return Response(
                    {
                        'message': 'Registration successful',
                        'token': token
                    },
                    status=status.HTTP_201_CREATED
                )
                
        return Response(user_to_create.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)


class LoginView(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        try:
            user_to_login = User.objects.get(email=email)
        except User.DoesNotExist:
            raise PermissionDenied({'message': 'Unauthorized'})

        if not user_to_login.check_password(password):
            raise PermissionDenied({'message': 'Invalid credentials'})

        expiry_time = datetime.now() + timedelta(days=7)
        token = jwt.encode(
            {
                'sub': user_to_login.id,
                'exp':  int(expiry_time.strftime('%s')),
                'type': user_to_login.user_type
            },
            settings.SECRET_KEY, 
            algorithm='HS256'
        )

        return Response({'token': token, 'message': f'Welcome back {user_to_login.username}!'})


class ProfileView(APIView):
    def get(self, request, user_pk):
        try:
            user = User.objects.get(pk=user_pk)
            serialized_user = PopulatedUserSerializer(user)
            return Response(serialized_user.data, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            raise NotFound()
