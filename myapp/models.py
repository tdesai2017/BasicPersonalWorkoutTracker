from django.db import models
from datetime import datetime

# Create your models here.

class day(models.Model):
    day_name = models.CharField(max_length=250, unique=True)


class workout(models.Model):
    workout_name = models.CharField(max_length=250, unique=True)
    day = models.ForeignKey(day, on_delete=models.CASCADE)

class info(models.Model):
    workout = models.ForeignKey(workout, on_delete=models.CASCADE)
    set_num = models.IntegerField()
    rep_num = models.IntegerField()
    weight = models.IntegerField()
    date = models.DateField()
    deleted = models.BooleanField(default=False)
    time_modified = models.DateTimeField(auto_now=True)
