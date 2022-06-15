from enum import unique
import json
from django.db import models
from django.http import JsonResponse

class User(models.Model):
  name = models.CharField(max_length=100, default="AnonymousUser")
  email = models.CharField(max_length=100, unique=True, primary_key=True)
  password = models.BinaryField(max_length=60)
  def __str__(self):
    return self.name

class Event(models.Model):
  name = models.CharField(max_length=100)
  date = models.DateTimeField()
  creator = models.ForeignKey(User, on_delete=models.CASCADE)
  def __str__(self):
    return self.name

class Participant(models.Model):
  name = models.CharField(max_length=100)
  email = models.CharField(max_length=100)
  event = models.ForeignKey(Event, on_delete=models.CASCADE)
  def __str__(self):
    return self.name