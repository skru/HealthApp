from rest_framework import exceptions, serializers
from djoser.conf import settings as djoser_settings
from django.core import exceptions as django_exceptions
from django.contrib.auth.password_validation import validate_password
from django.db import IntegrityError, transaction
from rest_framework import exceptions, serializers
from rest_framework.exceptions import ValidationError
from django.contrib.auth import authenticate, get_user_model

User = get_user_model()

class CustomTokenSerializer(serializers.ModelSerializer):
    auth_token = serializers.CharField(source="key")
    is_practitioner = serializers.SerializerMethodField()

    def get_is_practitioner(self, obj):
        is_practitioner = obj.user.profile.is_practitioner
        return is_practitioner

    class Meta:
        model = djoser_settings.TOKEN_MODEL
        fields = ("auth_token", "is_practitioner")


class CustomUserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(style={"input_type": "password"}, write_only=True)
    practitioner = serializers.CharField(write_only=True)

    def get_practitioner(self, obj):
        practitioner = obj.user.profile.practitioner
        return practitioner

    default_error_messages = {
        "cannot_create_user": djoser_settings.CONSTANTS.messages.CANNOT_CREATE_USER_ERROR
    }

    class Meta:
        model = User
        fields = tuple(User.REQUIRED_FIELDS) + (
            djoser_settings.LOGIN_FIELD,
            User._meta.pk.name,
            "password", "practitioner"
        )

    def validate(self, attrs):
        username = attrs.get("username")
        email = attrs.get("email")
        password = attrs.get("password")
        practitioner = attrs.get("practitioner")
        user = User(
        	username=username,
        	password=password,
        	email=email
        )
        try:
            validate_password(password, user)
        except django_exceptions.ValidationError as e:
            serializer_error = serializers.as_serializer_error(e)
            raise serializers.ValidationError(
                {"password": serializer_error["non_field_errors"]}
            )
        return attrs

    def create(self, validated_data):
        try:
            user = self.perform_create(validated_data)
        except IntegrityError:
            self.fail("cannot_create_user")
        return user

    def perform_create(self, validated_data):
        with transaction.atomic():
            user = User.objects.create_user(
            	username=validated_data.get("username"),
	        	password=validated_data.get("password"),
	        	email=validated_data.get("email")
        	)
            if djoser_settings.SEND_ACTIVATION_EMAIL:
                user.is_active = False
                user.save(update_fields=["is_active"])
            practitioner_username = validated_data.get("practitioner")
            user.profile.practitioner = User.objects.get(username=practitioner_username)
            user.profile.save()
        return user