from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password

from tutdb.models import User
from pqhub.backends import CustomUserModelBackend


class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'username', 'first_name', 'last_name', 'password', 'level', 'faculty', 'department')
        extra_kwargs = {'password': {'write_only': True}}

    def validate_password(self, value):
        # Validate the password using Django's built-in password validation
        validate_password(value)
        return value

    def create(self, validated_data):
        # Hash the password before creating the user
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user


class SchoolInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('level', 'faculty', 'department')


class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data.get("email", "")
        password = data.get("password", "")

        if email and password:
            # created a custom authentication method in backends.py
            custom_auth = CustomUserModelBackend()
            user = custom_auth.authenticate(self.context.get("request"), email=email, password=password)
            # print("user2", user)
            if user:
                return user
            else:
                raise serializers.ValidationError("Invalid credentials")
        else:
            raise serializers.ValidationError("Must include 'email' and 'password'")
