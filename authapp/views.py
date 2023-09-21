from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from rest_framework.permissions import IsAuthenticated
from django.conf import settings
from django.contrib.auth import authenticate
from django.utils.crypto import get_random_string
from django.core.mail import send_mail, BadHeaderError
from django.core.cache import cache  # import Django's cache
from pqhub.settings import DEFAULT_FROM_EMAIL
from tutdb.models import User, Token as CustomToken
from .serializers import (
    UserRegistrationSerializer, SchoolInfoSerializer, UserLoginSerializer
    )
from datetime import timedelta

class PersonalInfoRegistrationView(APIView):
    """
    View for handling user registration and email confirmation.

    POST: Registers a user, generates and sends an OTP token via email.

    Args:
        request (Request): The HTTP request object.
        format (str, optional): The format of the response.

    Returns:
        Response: HTTP response with status and data.
    """
    def post(self, request, format=None) -> Response:
        # Validate user registration data
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            # Generate unique tokens for user and OTP
            u_id = get_random_string(length=32)
            otp_token = get_random_string(length=6, allowed_chars='1234567890')

            # Cache the OTP token in Redis with a 5-minute expiration time
            cache.set(f"otp_{u_id}", otp_token, timeout=300)

            # Store registration data in the session
            request.session['registration_token'] = u_id
            request.session['personal_info'] = serializer.validated_data

            # Send registration email with OTP token
            email_sent = self.send_registration_email(otp_token, serializer.validated_data['email'])

            if email_sent:
                return Response({'token_sent': True}, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Failed to send email'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # def send_registration_email(self, otp_token, email) -> bool:
    #     """
    #     Send a registration confirmation email with the OTP token.

    #     Args:
    #         otp_token (str): The OTP token.
    #         email (str): The user's email address.

    #     Returns:
    #         bool: True if the email was sent successfully, False otherwise.
    #     """
    #     try:
    #         send_mail(
    #             'Registration Confirmation',
    #             f'Your registration token is: {otp_token}\n\nPlease enter this token in the next step of the registration process.\
    #                 \n\nIf you did not request this token, please ignore this email. \
    #                 \n\nThank you,\nTUTCOV TEAM',
    #             'TUTCOV TEAM',
    #             settings.DEFAULT_FROM_EMAIL,
    #             [email],
    #             fail_silently=False,
    #         )
    #         return True
    #     except BadHeaderError:
    #         return False

        
    def send_registration_email(self, otp_token, email):
        try:
            send_mail(
                'Registration Confirmation',
                f'Your registration token is: {otp_token}',
                settings.DEFAULT_FROM_EMAIL,
                [email],
                fail_silently=False,
            )
            return True  # Email sent successfully
        except BadHeaderError:
            return False  # Email sending failed


class SchoolInfoRegistrationView(APIView):
    """
    View for handling school information registration.

    POST: Registers a user with school information after OTP validation.

    Args:
        request (Request): The HTTP request object.
        format (str, optional): The format of the response.

    Returns:
        Response: HTTP response with status and data.
    """
    def post(self, request, format=None) -> Response:
        stored_token = request.session.get('registration_token')

        # Get the OTP from the request and compare it with the cached OTP
        otp_provided = request.data.get('otp')
        otp_cached = cache.get(f"otp_{stored_token}")

        if not otp_provided or otp_provided != otp_cached:
            return Response({'detail': 'Invalid or expired OTP.'}, status=status.HTTP_400_BAD_REQUEST)

        # Validate school information
        serializer = SchoolInfoSerializer(data=request.data)
        if serializer.is_valid():
            # Combine user data with personal info from the session
            user_data = {**serializer.validated_data, **request.session.get('personal_info')}

            # Remove session data
            del request.session['registration_token']
            del request.session['personal_info']

            # Create the user with school information
            user = User.objects.create_user(**user_data)
            return Response({'user_id': user.id}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

from django.contrib import auth

class UserLoginView(APIView):
    def post(self, request, format=None):
        serializer = UserLoginSerializer(data=request.data, context={"request": request})

        if serializer.is_valid():
            print(serializer.validated_data)
            user = serializer.validated_data


            if user is not None:
                # User is valid, create access and refresh tokens
                refresh = RefreshToken.for_user(user)
                access_token = AccessToken.for_user(user)

                print(refresh)
                print(access_token)

                # Store tokens in CustomToken model
                custom_token, _ = CustomToken.objects.get_or_create(user=my_user)
                custom_token.access_token = str(access_token)
                custom_token.refresh_token = str(refresh)
                # custom_token.access_token_expires_at = access_token['exp']
                # custom_token.refresh_token_expires_at = refresh['exp']

                # custom_token.access_token_expires_at = timedelta(minutes=30)
                # custom_token.refresh_token_expires_at = timedelta(hours=12)
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
