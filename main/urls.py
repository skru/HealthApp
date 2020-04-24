# from django.conf.urls import include
from django.urls import path
from django.contrib import admin
from django.conf import settings
from django.conf.urls import url, include
from django.contrib.auth.models import User
from django.http import Http404
from rest_framework import routers, serializers, viewsets, generics, mixins 
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from nhs.models import *
from chat.models import *
from main.serializers import *


from django.db import IntegrityError, transaction
import traceback




# ViewSets define the view behavior.
class PractitionerViewSet(viewsets.ModelViewSet):
    lookup_field = 'username'
    queryset = User.objects.filter(profile__is_practitioner=True)
    serializer_class = PractitionerSerializer

class NHSConditionViewSet(viewsets.ModelViewSet):
    queryset = NHSCondition.objects.all()
    serializer_class = NHSConditionSerializer
    http_method_names = ['get']

class ChatViewSet(generics.ListCreateAPIView):
    queryset = Chat.objects.all()
    serializer_class = ChatSerializer
    http_method_names = ['get']
    permission_classes = [IsAuthenticated]

    def list(self, request, username):
        queryset = self.get_queryset()
        user = User.objects.get(username=username)
        if queryset.filter(participants__in=[user]).exists():
            queryset = queryset.filter(participants__in=[user])
            serializer = ChatSerializer(queryset, many=True)
            return Response(serializer.data)

        new_chat = Chat.objects.create()
        new_chat.participants.add(user, user.profile.practitioner)
        new_chat.save()
        queryset = queryset.filter(participants__in=[user])
        serializer = ChatSerializer(queryset, many=True)
        return Response(serializer.data)


# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'practitioners', PractitionerViewSet)
router.register(r'conditions', NHSConditionViewSet)
#router.register(r'chats', ChatViewSet, basename="ChatViewSet")

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.

alt_url = ""
if (settings.DEBUG == True):
    alt_url = "api/"

urlpatterns = [
	#path(alt_url + 'chat/', include('chat.urls')),
    path(alt_url + 'admin/', admin.site.urls),
    path(alt_url + '', include(router.urls)),
    url(alt_url + r'chats/(?P<username>[\w.@+-]+)/$', ChatViewSet.as_view()),
    path(alt_url + 'api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path(alt_url + 'auth/', include('djoser.urls')),
    path(alt_url + 'auth/', include('djoser.urls.authtoken')),
]