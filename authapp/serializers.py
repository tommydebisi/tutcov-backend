from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from tutdb.models import User


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
    class Meta:
        model = User
        fields = ('email', 'password')