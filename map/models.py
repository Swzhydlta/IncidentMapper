from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    pass


class Incident(models.Model):
    typeOf = models.CharField(max_length=20)
    timestamp = models.DateTimeField(auto_now_add=False)
    lat = models.FloatField()
    long = models.FloatField()
    description = models.CharField(max_length=2000)
    beingEdited = models.BooleanField(default=False)

    def serialize(self):
        return {
            "id": self.id,
            "typeOf": self.typeOf,
            "timestamp": self.timestamp,
            "lat": self.lat,
            "long": self.long,
            "description": self.description,
            "beingEdited": self.beingEdited,
        }

class editRequest(models.Model):
    targetPost = models.IntegerField()
    description = models.CharField(max_length=2000)

    def serialize(self):
        return {
            "id": self.id,
            "targetPost": self.targetPost,
            "description": self.description,
        }


