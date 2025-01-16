from django.db import models

class Building(models.Model):
    """Building model"""
    name = models.CharField(max_length=100)  # Adjusted max_length to be more practical

    def __str__(self):
        return self.name


class Room(models.Model):
    """Room model"""
    roomNum = models.CharField(max_length=20)
    building = models.ForeignKey(
        Building, on_delete=models.CASCADE, related_name='rooms'
    )
    meetings = models.JSONField()

    def __str__(self):
        return f"Room {self.roomNum} in {self.building.name}"

