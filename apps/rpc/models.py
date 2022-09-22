from django.db import models

# Create your models here.

class ElectraAPIModel(models.Model):
    session_id = models.CharField(max_length=64)
    ts = models.DateTimeField('timestamp')