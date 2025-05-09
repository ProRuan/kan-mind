
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
    RegistrationSerializer,
    LoginSerializer,
    UserEmailCheckSerializer,
)


class RegistrationView(APIView):
    """
    Handle user registration and return auth token with user info.
    """
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)
        if not serializer.is_valid():
            return self._error_response(serializer)

        user = serializer.save()
        return self._success_response(user, status.HTTP_201_CREATED)

    def _success_response(self, user, code):
        token, _ = Token.objects.get_or_create(user=user)
        return Response({
            "token": token.key,
            "fullname": f"{user.first_name} {user.last_name}".strip(),
            "email": user.email,
            "user_id": user.id
        }, status=code)

    def _error_response(self, serializer):
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    """
    Authenticate a user and return auth token with user info.
    """
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if not serializer.is_valid():
            return self._error_response(serializer)

        user = serializer.validated_data["user"]
        return self._success_response(user, status.HTTP_200_OK)

    def _success_response(self, user, code):
        token, provided = Token.objects.get_or_create(user=user)
        return Response({
            "token": token.key,
            "fullname": f"{user.first_name} {user.last_name}".strip(),
            "email": user.email,
            "user_id": user.id
        }, status=code)

    def _error_response(self, serializer):
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EmailCheckView(APIView):
    """
    Check if a given email exists and return associated user info.
    """
    permission_classes = [permissions.IsAuthenticated]
    email_pattern = re.compile(r"^\S+@\S+\.\S+$")

    def get(self, request):
        email = request.query_params.get('email')
        if not email:
            return self._missing_email_response()

        if not self.email_pattern.match(email):
            return self._invalid_email_response()

        return self._get_user_response(email)

    def _missing_email_response(self):
        return Response(
            {"detail": "The 'email' query parameter is required."},
            status=status.HTTP_400_BAD_REQUEST
        )

    def _invalid_email_response(self):
        return Response(
            {"detail": "Please enter a valid email address."},
            status=status.HTTP_400_BAD_REQUEST
        )

    def _get_user_response(self, email):
        try:
            user = User.objects.get(email=email)
            serializer = UserEmailCheckSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({}, status=status.HTTP_200_OK)
