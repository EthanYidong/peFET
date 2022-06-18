from django.db import models


class User(models.Model):
    name = models.CharField(max_length=100, default="AnonymousUser")
    email = models.CharField(max_length=100, unique=True)
    password = models.BinaryField(max_length=60)

    def __str__(self):
        return self.email


class Event(models.Model):
    name = models.CharField(max_length=100)
    date = models.DateField()
    creator = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Participant(models.Model):
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
