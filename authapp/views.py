from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from rest_framework.permissions import IsAuthenticated, AllowAny
from authapp.serializers import ProfileSerializer
from django.conf import settings
from django.utils.crypto import get_random_string
from django.core.mail import send_mail, BadHeaderError
from django.core.cache import cache  # import Django's cache

from authapp.models import User, Token as CustomToken, Profile
from .serializers import (
    UserRegistrationSerializer, SchoolInfoSerializer, UserLoginSerializer
    )
from datetime import timedelta
from django.utils import timezone
from drf_spectacular.utils import extend_schema

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
    @extend_schema(responses=UserRegistrationSerializer, description=
                   "View for handling user registration and email confirmation.POST: Registers a user, generates and sends an OTP token via email.Args:request (Request): The HTTP request object.format (str, optional): The format of the response. Returns:Response: HTTP response with status and data.")
    def post(self, request, format=None) -> Response:
        # Validate user registration data
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            # Generate unique tokens for user and OTP (length=5)
            u_id = get_random_string(length=32)
            otp_token = get_random_string(length=5, allowed_chars='1234567890')

            # Cache the OTP token in Redis with a 5-minute expiration time
            cache.set(f"otp_{u_id}", otp_token, timeout=300)

            # Store registration data in the session
            request.session['registration_token'] = u_id
            request.session['personal_info'] = serializer.validated_data

            # Send registration email with OTP token
            # email_sent = self.send_registration_email(otp_token, serializer.validated_data['email'])

            # if email_sent:
            #     return Response({'token_sent': True}, status=status.HTTP_200_OK)
            # else:
            serializer.save()
            return Response({'Success': 'Account creation successful'}, status=status.HTTP_201_CREATED)
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
    @extend_schema(responses=SchoolInfoSerializer, description=
                   "View for handling school information registration.POST: Registers a user with school information after OTP validation.Args:request (Request): The HTTP request object. format (str, optional): The format of the response. Returns:Response: HTTP response with status and data.")
    def post(self, request, format=None) -> Response:
        stored_token = request.session.get('registration_token')

        # Get the OTP from the request and compare it with the cached OTP
        otp_provided = request.data.get('otp')
        print(otp_provided)
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
    
    @extend_schema(responses=UserLoginSerializer, description="Generates access and refresh tokens for a user")
    def post(self, request, format=None):
        """
        View for logging in only registered users.

        POST: Logs in a user with information provided after validation and create access and refresh tokens.

        Args:
            request (Request): The HTTP request object.
            format (str, optional): The format of the response.

        Returns:
            Response: HTTP response with status and data.
        """
        serializer = UserLoginSerializer(data=request.data, context={"request": request})

        if serializer.is_valid():
            # print(serializer.validated_data)
            user = serializer.validated_data

            my_user = User.objects.get(email=user)

            if user is not None:
                # User is valid, create access and refresh tokens
                refresh = RefreshToken.for_user(user)
                access_token = AccessToken.for_user(user)

                # Store tokens in CustomToken model
                custom_token, _ = CustomToken.objects.get_or_create(user=my_user)
                custom_token.access_token = str(access_token)
                custom_token.refresh_token = str(refresh)
                custom_token.access_token_expires_at = timezone.now() + timedelta(minutes=30)
                custom_token.refresh_token_expires_at = timezone.now() + timedelta(hours=12)

                custom_token.save()

                return Response({
                    'access_token': str(access_token),
                }, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLogoutView(APIView):
    """View to log out the current user."""
    permission_classes = [AllowAny]

    def post(self, request, format=None):
        # Get the access token from the Authorization header
        auth_header = request.META.get('HTTP_AUTHORIZATION')
        if auth_header and auth_header.startswith('Bearer '):
            access_token = auth_header[len('Bearer '):]
            access_token_obj = AccessToken(access_token)

            # Check if the access token is associated with the current user
            user_instance = User.objects.get(email=request.user.email)
            custom_token = CustomToken.objects.filter(user=user_instance).first()
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
        # print(auth_header)
        if auth_header and auth_header.startswith('Bearer '):
            access_token = auth_header[len('Bearer '):]
            
    
            current_user = User.objects.get(email=request.user.email)
            print("current_user", current_user)
            custom_token = CustomToken.objects.filter(user=current_user, access_token=access_token).first()
            print(custom_token)
            if custom_token:
                # Generate a new access token based on the refresh token
                refresh_token = RefreshToken(custom_token.refresh_token)
                new_access_token = AccessToken.for_user(request.user)

                # Update the CustomToken model with the new access token
                custom_token.access_token = str(new_access_token)
                custom_token.access_token_expires_at = timezone.now() + timedelta(minutes=30)
                custom_token.save()

                # Return the newly created access token in the response
                return Response({'access_token': str(new_access_token)}, status=status.HTTP_200_OK)

        # If the access token is invalid, not associated, or other errors occur, respond with an error
        return Response({'error': 'Invalid access token or user not authenticated'}, status=status.HTTP_400_BAD_REQUEST)
    


class UserProfileView(APIView):
    """Only authenticated users can access this page."""
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None, **kwargs):
        user = User.objects.get(email=request.user.email)
        profile = Profile.objects.get(user=user)
        serializer = ProfileSerializer(profile)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def put(self, request, format=None, **kwargs):
        """The user gets to view and edit their information on the application."""
        user = User.objects.get(email=request.user.email)
        profile = Profile.objects.get(user=user)
        serializer = ProfileSerializer(profile, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    
