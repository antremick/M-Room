from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Room
from .serializers import RoomSerializer

# Create your views here.
class Room(APIView):
    def get(self, request):
        Rooms = Room.objects.all()
        serializer = RoomSerializer(Rooms, many=True)
        return Response(serializer.data)