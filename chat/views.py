from django.shortcuts import render
from django.template import RequestContext
from django.conf import settings

def index(request):
    return render(request, 'chat/index.html', {})

def room(request, room_name):
    return render(request, 'chat/room.html', {
        'room_name': room_name,
        'unsecure_socket': settings.DEBUG
    })