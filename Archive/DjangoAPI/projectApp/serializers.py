from rest_framework import serializers
from .models import Room, Building

class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ['RoomNum', 'Building', 'Meetings']

class BuildingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Building
        fields = ['Building']