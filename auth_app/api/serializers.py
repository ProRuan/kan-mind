# Third-party imports
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

User = get_user_model()


class RegistrationSerializer(serializers.ModelSerializer):
    """
    Serializer for user registration.

    Accepts full name, email, password, and repeated password.
    Splits full name into first and last name.
    """

    fullname = serializers.CharField(
        write_only=True,
        required=True,
        help_text="Full name of the user (first and last name)."
    )
    password = serializers.CharField(
        write_only=True,
        required=True,
        style={"input_type": "password"},
        help_text="Password for the user account."
    )
    repeated_password = serializers.CharField(
        write_only=True,
        required=True,
        style={"input_type": "password"},
        help_text="Repeat the password to confirm."
    )

    class Meta:
        model = User
        fields = ['fullname', 'email', 'password', 'repeated_password']

    def validate_email(self, value):
        """
        Ensure the email is unique.
        """
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError(
                "A user with this email already exists."
            )
        return value

    def validate_password(self, value):
        """
        Validate password against Django's password validators.
        """
        validate_password(value)
        return value

    def validate(self, data):
        """
        Ensure both passwords match.
        """
        if data['password'] != data['repeated_password']:
            raise serializers.ValidationError({
                "repeated_password": "Passwords do not match."
            })
        return data

    def create(self, validated_data):
        """
        Create and return a new user instance.
        """
        fullname = validated_data.pop('fullname')
        password = validated_data.pop('password')
        validated_data.pop('repeated_password')

        first_name, last_name = self._split_fullname(fullname)

        user = self._get_user(
            username=fullname,
            email=validated_data['email'],
            first_name=first_name,
            last_name=last_name,
            password=password
        )
        user.save()
        return user

    def _split_fullname(self, fullname):
        """
        Split a full name into first and last name.
        """
        name_parts = fullname.strip().split()
        first_name, *rest = name_parts
        last_name = " ".join(rest)
        return first_name, last_name

    def _get_user(self, username, email, first_name, last_name, password):
        """
        Return a new user instance with a set password.
        """
        user = User(
            username=username,
            email=email,
            first_name=first_name,
            last_name=last_name
        )
        user.set_password(password)
        return user


class LoginSerializer(serializers.Serializer):
    """
    Serializer for user login.

    Authenticates user with email and password.
    """

    email = serializers.EmailField(
        write_only=True,
        required=True,
        help_text="User's registered email address."
    )
    password = serializers.CharField(
        write_only=True,
        required=True,
        style={"input_type": "password"},
        help_text="User's account password."
    )

    def validate(self, data):
        """
        Validate user credentials and authenticate the user.

        Raises:
            serializers.ValidationError: If email does not exist or authentication fails.
        """
        email = data.get("email")
        password = data.get("password")

        user = self._get_user_by_email(email)
        user = authenticate(username=user.username, password=password)

        if not user:
            raise serializers.ValidationError("Invalid email or password.")

        data["user"] = user
        return data

    def _get_user_by_email(self, email):
        """
        Retrieve a user instance by email or raise a validation error.
        """
        try:
            return User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError("Invalid email or password.")


class UserEmailCheckSerializer(serializers.ModelSerializer):
    """
    Serializer for checking if a user email exists.

    Returns user ID, email, and full name.
    """

    fullname = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'email', 'fullname']

    def get_fullname(self, obj):
        """
        Concatenate first and last name.
        """
        return f"{obj.first_name} {obj.last_name}".strip()
