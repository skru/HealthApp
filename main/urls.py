# from django.conf.urls import include
from django.urls import path
from django.contrib import admin
from django.conf import settings

# urlpatterns = [
#     path('chat/', include('chat.urls')),
#     path('admin/', admin.site.urls),
#     path('api-auth/', include('rest_framework.urls')),
# ]


from django.conf.urls import url, include
from django.contrib.auth.models import User
from rest_framework import routers, serializers, viewsets

# Serializers define the API representation.
class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'is_staff']

# ViewSets define the view behavior.
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'users', UserViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.

alt_url = ""
if (settings.DEBUG == True):
    alt_url = "api/"

urlpatterns = [
	#path(alt_url + 'chat/', include('chat.urls')),
    path(alt_url + 'admin/', admin.site.urls),
    path(alt_url + '', include(router.urls)),
    path(alt_url + 'api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path(alt_url + 'auth/', include('djoser.urls')),
    path(alt_url + 'auth/', include('djoser.urls.authtoken')),
    #path(alt_url + 'dj-rest-auth/', include('dj_rest_auth.urls')),
    #path(alt_url + 'dj-rest-auth/registration/', include('dj_rest_auth.registration.urls'))
]