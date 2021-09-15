from django.db import models

# Create your models here.

class History(models.Model):
    origin = models.CharField(max_length=32)
    destination = models.CharField(max_length=32)
    dist = models.CharField(max_length=16)
    def __str__(self):
        return self.origin+" to "+self.destination