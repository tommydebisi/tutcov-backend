from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from rest_framework.permissions import IsAuthenticated

from django.contrib.auth import authenticate
from django.utils.crypto import get_random_string
from django.core.mail import send_mail, BadHeaderError

from tutdb.models import User, Token as CustomToken
from .serializers import (
    UserRegistrationSerializer, SchoolInfoSerializer, UserLoginSerializer
    )


class PersonalInfoRegistrationView(APIView):
    def post(self, request, format=None):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            # Generate a unique token and store it in the user's session
            # TODO: implement number token, length of 6
            # TODO: implement token expiration with redis
            token = get_random_string(length=32)
            request.session['registration_token'] = token
            request.session['personal_info'] = serializer.validated_data
            
            # Send the token to the user's email
            email_sent = self.send_registration_email(token, serializer.validated_data['email'])
            
            if email_sent:
                return Response({'token_sent': True}, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Failed to send email'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def send_registration_email(self, token, email):
        try:
            send_mail(
                'Registration Confirmation',
                f'Your registration token is: {token}',
                'from@example.com',
                [email],
                fail_silently=False,
            )
            return True  # Email sent successfully
        except BadHeaderError:
            return False  # Email sending failed


class SchoolInfoRegistrationView(APIView):
    def post(self, request, format=None):
        token = request.data.get('token')
        stored_token = request.session.get('registration_token')
        if not token or token != stored_token:
            return Response({'detail': 'Invalid or expired token.'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = SchoolInfoSerializer(data=request.data)
        if serializer.is_valid():
            # Registration is complete, remove the token from the session
            del request.session['registration_token']
            # Create the user with both personal and school info
            user_data = {**serializer.validated_data, **request.session.get('personal_info')}
            print(user_data)
            user = User.objects.create_user(**user_data)
            return Response({'user_id': user.id}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

from django.contrib import auth

class UserLoginView(APIView):
    def post(self, request, format=None):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            print("hereee")
            print(request.data)
            email = request.data['email']
            password = request.data['password']
            current_user = User.objects.get(email=email)
            user = auth.login(request, current_user)

            if user is not None:
                # User is valid, create access and refresh tokens
                refresh = RefreshToken.for_user(user)
                access_token = AccessToken.for_user(user)

                # Store tokens in CustomToken model
                custom_token, _ = CustomToken.objects.get_or_create(user=user)
                custom_token.access_token = str(access_token)
                custom_token.refresh_token = str(refresh)
                custom_token.access_token_expires_at = access_token['exp']
                custom_token.refresh_token_expires_at = refresh['exp']
                custom_token.save()

                return Response({
                    'access_token': str(access_token),
                }, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        # Get the access token from the Authorization header
        auth_header = request.META.get('HTTP_AUTHORIZATION')
        if auth_header and auth_header.startswith('Bearer '):
            access_token = auth_header[len('Bearer '):]
            access_token_obj = AccessToken(access_token)

            # Check if the access token is associated with the current user
            if access_token_obj['user_id'] == str(request.user.id):
                # Delete the CustomToken model associated with the current user
                custom_token = CustomToken.objects.filter(user=request.user).first()
                if custom_token:
                    custom_token.delete()

                return Response({'message': 'User successfully logged out'}, status=status.HTTP_200_OK)

        # If the access token is invalid or not associated, respond with an error
        return Response({'error': 'Invalid access token or user not authenticated'}, status=status.HTTP_400_BAD_REQUEST)


class TokenResetView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        # Get the access token from the Authorization header
        auth_header = request.META.get('HTTP_AUTHORIZATION')
        if auth_header and auth_header.startswith('Bearer '):
            access_token = auth_header[len('Bearer '):]

            # Check if the access token is associated with the current user
            custom_token = CustomToken.objects.filter(user=request.user, access_token=access_token).first()
            if custom_token:
                # Generate a new access token based on the refresh token
                refresh_token = RefreshToken(custom_token.refresh_token)
                new_access_token = AccessToken.for_user(request.user)

                # Update the CustomToken model with the new access token
                custom_token.access_token = str(new_access_token)
                custom_token.access_token_expires_at = new_access_token['exp']
                custom_token.save()

                # Return the newly created access token in the response
                return Response({'access_token': str(new_access_token)}, status=status.HTTP_200_OK)

        # If the access token is invalid, not associated, or other errors occur, respond with an error
        return Response({'error': 'Invalid access token or user not authenticated'}, status=status.HTTP_400_BAD_REQUEST)
