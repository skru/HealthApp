from rest_framework import exceptions, serializers
from djoser.conf import settings as djoser_settings

class CustomTokenSerializer(serializers.ModelSerializer):
    auth_token = serializers.CharField(source="key")
    is_practitioner = serializers.SerializerMethodField()

    def get_is_practitioner(self, obj):
        is_practitioner = obj.user.profile.is_practitioner
        return is_practitioner

    class Meta:
        model = djoser_settings.TOKEN_MODEL
        fields = ("auth_token", "is_practitioner")