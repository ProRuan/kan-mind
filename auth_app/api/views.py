# 1. Standard library
import re

# 2. Third-party suppliers
from django.contrib.auth.models import User
from rest_framework import permissions, status
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

# 3. Local imports
from .serializers import (
    LoginSerializer,
    RegistrationSerializer,
    UserEmailCheckSerializer,
)


class BaseAuthView(APIView):
    """
    Base class for user authentication and registration.

    Provides helper methods for generating success and error responses.
    """

    def _get_success_response(self, user, code):
        """
        Generate a success response with user info and auth token.

        Args:
            user (User): The authenticated or newly registered user.
            code (int): HTTP status code to return with the response.

        Returns:
            Response: The success response containing the token and user info.
        """
        token, provided = Token.objects.get_or_create(user=user)
        return Response({
            "token": token.key,
            "fullname": f"{user.first_name} {user.last_name}".strip(),
            "email": user.email,
            "user_id": user.id
        }, status=code)

    def _get_error_response(self, serializer):
        """
        Generate an error response for invalid serializer data.

        Args:
            serializer (serializers.Serializer): The serializer with validation errors.

        Returns:
            Response: The error response containing serializer errors.
        """
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RegistrationView(BaseAuthView):
    """
    Handle user registration and return auth token with user info.

    Allows users to register with a full name, email, and password. After
    registration, an authentication token and user details are returned.
    """
    permission_classes = [AllowAny]

    def post(self, request):
        """
        Handle POST request for user registration.

        Args:
            request (Request): The request containing user registration data.

        Returns:
            Response: The success or error response based on the validity of the data.
        """
        serializer = RegistrationSerializer(data=request.data)
        if not serializer.is_valid():
            return self._get_error_response(serializer)

        user = serializer.save()
        return self._get_success_response(user, status.HTTP_201_CREATED)


class LoginView(BaseAuthView):
    """
    Authenticate a user and return auth token with user info.

    Allows users to log in with their email and password. After authentication,
    an authentication token and user details are returned.
    """
    permission_classes = [AllowAny]

    def post(self, request):
        """
        Handle POST request for user login.

        Args:
            request (Request): The request containing user login credentials.

        Returns:
            Response: The success or error response based on the validity of the data.
        """
        serializer = LoginSerializer(data=request.data)
        if not serializer.is_valid():
            return self._get_error_response(serializer)

        user = serializer.validated_data["user"]
        return self._get_success_response(user, status.HTTP_200_OK)


class EmailCheckView(APIView):
    """
    Check if a given email exists and return associated user info.

    Allows authenticated users to check if a specific email is already in use. 
    If the email exists, it returns the associated user details.
    """
    permission_classes = [permissions.IsAuthenticated]
    email_pattern = re.compile(r"^\S+@\S+\.\S+$")

    def get(self, request):
        """
        Handle GET request for checking if an email exists.

        Args:
            request (Request): The request containing the 'email' query parameter.

        Returns:
            Response: A response with user information if the email exists, or an error.
        """
        email = request.query_params.get('email')
        if not email:
            return self._missing_email_response()

        if not self.email_pattern.match(email):
            return self._invalid_email_response()

        return self._get_user_response(email)

    def _missing_email_response(self):
        """
        Generate a response indicating that the 'email' query parameter is missing.

        Returns:
            Response: The error response indicating the missing email.
        """
        return Response(
            {"detail": "The 'email' query parameter is required."},
            status=status.HTTP_400_BAD_REQUEST
        )

    def _invalid_email_response(self):
        """
        Generate a response indicating that the provided email is invalid.

        Returns:
            Response: The error response indicating the invalid email.
        """
        return Response(
            {"detail": "Please enter a valid email address."},
            status=status.HTTP_400_BAD_REQUEST
        )

    def _get_user_response(self, email):
        """
        Retrieve a user instance by email and return the associated user info.

        Args:
            email (str): The email address to check.

        Returns:
            Response: A response with user data if the email exists, or an empty response.
        """
        try:
            user = User.objects.get(email=email)
            serializer = UserEmailCheckSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({}, status=status.HTTP_200_OK)
